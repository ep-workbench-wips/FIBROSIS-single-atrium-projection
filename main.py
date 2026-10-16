from sklearn.neighbors import KDTree
import pyvista as pv
import numpy as np
import openep

try:

    debug = False
    print(case_1)
    case_model=cases[case_1]
    case_RA=cases[case_2]
    print("Running in PROD mode", flush=True)


except NameError:
    print("DEBUG MODE: Please run this is PROD mode in EP Workbench WIP.",  flush=True)
    case_model_path = "/Users/vinush-vigneswaran/Documents/09_DATASETS/openep_dataset_2.mat"
    case_LA_path = "/Users/vinush-vigneswaran/Documents/09_DATASETS/openep_dataset_2.mat"

    case_model = openep.load_openep_mat(case_model_path)
    case_eam = openep.load_openep_mat(case_LA_path)

    display_plot = True
    field_name = 'bipolar_voltage'
    above_threshold = False
    threshold = 0.5

def main():

    ######### Read Mesh File ###########
    mesh_model = case_model.create_mesh()
    print("Loaded case_model", flush=True)

    mesh_eam = case_eam.create_mesh()
    mesh_eam['bip'] = case_eam.fields[f'{field_name}']
    print("Loaded mesh", flush=True)

    # project using kd tree
    mesh_elem_centers = mesh_model.cell_centers()
    f_tree = KDTree(mesh_eam.points,leaf_size = 2)
    dist, ind = f_tree.query(mesh_elem_centers.points, k=1)
    print("Project using kd tree", flush=True)

    # # apply bip
    # case_model.fields.bipolar_voltage = merged_eam_mesh['bip'][ind]

    # convert to binary
    mesh_elem = np.ndarray((len(mesh_elem_centers.points), 1), dtype=float)
    fibrosis_mask = np.ndarray((len(mesh_elem_centers.points)),dtype=bool)
    for i in range(len(dist)):

        progress = int(100 * i/len(dist))
        if i % 50000 == 0:
            print(f'Progress: {progress}', flush=True)

        mesh_elem[i] = mesh_eam['bip'][ind[i]][0]
        field_data = mesh_eam['bip'][ind[i]][0]
        if above_threshold and field_data <= threshold and field_data > 0:
            fibrosis_mask[i] = True
        elif not above_threshold and field_data >= threshold and field_data > 0:
            fibrosis_mask[i] = True
        else:
            fibrosis_mask[i] = False

    print("Created binary mask", flush=True)


    # check cell_regions exist in model
    if case_model.fields.cell_region is None:
        case_model.fields.cell_region = np.zeros(len(case_model.indices), dtype=int)

    # apply region 46 to cell region
    cell_regions = []
    for i in range(len(case_model.indices)):
        if fibrosis_mask[i]:
            cell_regions.append(46)
        else:
            cell_regions.append(case_model.fields.cell_region[i])

    case_model.fields.cell_region = np.array(cell_regions)

    # display mesh
    if display_plot:
        new_mesh_model = case_model.create_mesh()
        show_mesh(new_mesh_model, case_model.fields[field_name], clim=[0, threshold])
        show_mesh(new_mesh_model, case_model.fields.cell_region, clim=[0, 45])

    print("Outputting new case", flush=True)
    out_cases[f'{case_1}_fibrosis'] = case_model

def show_mesh(mesh, scalar = None, clim = None):
    """Plot"""
    p = pv.Plotter()

    if scalar is not None:
        p.add_mesh(mesh, scalars=scalar, clim=clim, above_color='pink')
    else:
        p.add_mesh(mesh)
    p.show()


if __name__ == '__main__':
    main()
# show_mesh(case_model.create_mesh(), case_model.fields.cell_region)



