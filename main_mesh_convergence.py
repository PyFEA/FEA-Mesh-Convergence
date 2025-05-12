"""
FEA Automation -  Example of mesh convergence study with Python and Abaqus

"""
import os
import fea_tools
import numpy as np
import matplotlib.pyplot as plt

# 1) Input Parameters
elem_size = 6
max_iter= 10

# Template input file
template_file = 'StaticBeam_template.inp'

# Main directories: workdir and temporary
wdir = os.getcwd()
print('wdir:', wdir)
tdir = os.path.join(wdir, 'temp')
print('tdir:', tdir)
os.makedirs(tdir, exist_ok=True)

results = dict()

for i in range(max_iter):
    
    jobname = f'Static_ElemSize_{elem_size:.2f}'.replace('.','p') 

    current_elem_size = elem_size
    # 2) Preprocess input file and run simulation
    fea_tools.run_mesh_convergence(jobname=jobname,elem_size=elem_size,template_file=template_file, wdir=wdir, tdir=tdir)

    # Smaller element size for next iteration
    elem_size /= 1.3

    # 3) Read results (monitored dof from .sta file)
    sta_file = os.path.join(tdir, jobname + '.sta')
    dof_value = fea_tools.postprocess_mesh_convergence(sta_file=sta_file)

    results[current_elem_size] = dof_value

print(results)


# Export table with results
sorted_results = []
for key in sorted(results.keys(), reverse=True): # Sort in descending ELsize
    value = results[key]
    sorted_results.append((key, value))

print(sorted_results)

np.savetxt('ElemSize_VS_UY.txt', sorted_results,
           header=f'{"Element Size":>10s} {"UY":>8s}',
           fmt=('%12.4f','%12.4f'))


# Plot results
# Convert to NumPy array for plotting
results_array = np.array(sorted_results)

element_sizes = results_array[:, 0]
UY_values = results_array[:, 1]

plt.figure()
plt.plot(element_sizes, UY_values, 'o-', label='Monitored DOF (UY)')
plt.xlabel('Element Size')
plt.ylabel('UY at Monitored Node')
plt.title('Mesh Convergence Study')
plt.grid(True)
plt.legend()
plt.gca().invert_xaxis()  # Smaller elements to the right
plt.tight_layout()
plt.savefig('Mesh_Conv.pdf')
plt.show()