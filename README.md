
# Mesh Convergence Study Automation with Python and Abaqus  

This project automates a **finite element mesh convergence study** using **Python** and **Abaqus**. It generates parametric 2D rectangular meshes with **Gmsh**, runs static simulations in **Abaqus/Standard**, extracts a monitored displacement from the `.sta` file, and produces convergence plots and results tables.

---

# Project Structure

```
.
├── fea_tools.py                # Preprocessing, simulation, and postprocessing functions
├── meshing.py                  # Structured rectangular mesh generator using Gmsh
├── StaticBeam_template.inp     # Abaqus input file template with placeholders
├── temp/                       # Temporary directory for job input and output files
├── ElemSize_VS_UY.txt          # Exported results table
├── Mesh_Conv.pdf               # Convergence plot
└── main.py                     # Main driver script
```

---

# Features

- Automated parametric mesh generation (`rectangle_mesh`)
- Editable Abaqus input templates with mesh and boundary conditions injected
- Batch simulation of decreasing element sizes
- Displacement extraction from `.sta` file (DOF monitor)
- Result export and convergence plot generation with `matplotlib`

---

# Requirements

- **Python 3.x**
- **Gmsh** (with Python API installed)
- **Abaqus 2024** (or update `ABQ_CMD` in `fea_tools.py`)
- Python libraries: `numpy`, `matplotlib`

Install Python dependencies:
```bash
pip install numpy matplotlib
```

---

# How to Run

1. Set the Abaqus command in `fea_tools.py`:
   ```python
   ABQ_CMD = 'abq2024'  # Or full path to Abaqus launcher
   ```

2. Ensure `Gmsh` is installed and accessible via its Python API.

3. Run the main script:
   ```bash
   python main.py
   ```

This will:
- Run a mesh convergence loop
- Save the results to `ElemSize_VS_UY.txt`
- Plot the mesh convergence curve to `Mesh_Conv.jpeg`

---

# Output Example

```
ElemSize_VS_UY.txt:
Element Size       UY
     6.0000    -0.2880
     4.6154    -0.2802
     3.5503    -0.2748
     ...
```

Convergence plot:

Mesh_Conv.jpeg

---

# Notes

- The template file `StaticBeam_template.inp` must contain placeholders:
  - `<BEAM_MESH>` – mesh bulk
  - `<ASSEMBLY_SETS>` – physical group sets
  - `<JOBNAME>` – job name string
- Mesh size decreases by a factor of 1.3 each iteration, can be adjusted.

---

# License

This project is intended for educational and engineering demonstration purposes.
