# Fibrosis Single Atrium Projection

## Overview

This script maps electroanatomical mapping (EAM) voltage data onto a target cardiac mesh using a KDTree nearest-neighbour search.

It applies a voltage threshold to identify specific regions and assigns **region ID 46** to the corresponding mesh cells.

## How It Works

1. Loads the target mesh and EAM data.
2. Uses a KDTree to find the nearest EAM point for each target mesh cell.
3. Applies a voltage threshold to create a binary mask.
4. Assigns region ID `46` to cells meeting the threshold criteria.
5. Optionally displays the voltage and region maps.
6. Outputs the updated case as `<case_name>_fibrosis`.

## Parameters

- `field_name`: EAM field to use (default: `bipolar_voltage`).
- `threshold`: Voltage threshold (default: `0.5`).
- `above_threshold`: If `True`, selects values between 0 and the threshold. If `False`, selects values greater than or equal to the threshold.
- `display_plot`: Whether to display the resulting meshes.

## Requirements

- `numpy`
- `scikit-learn`
- `pyvista`
- `openep`

## Usage

Run the script in **EP Workbench WIP** with the target model and EAM case selected.

The updated case will be available in `out_cases` with the suffix `_fibrosis`.

**Note:** Existing cell region labels are preserved for cells that do not meet the threshold criteria.