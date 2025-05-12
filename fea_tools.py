"""
FEA Automation Tools

"""
# Import libraries and functions
import shutil
import subprocess
import os
from meshing import rectangle_mesh


ABQ_CMD = 'abq2024' # ABQ_CMD = R'c:\SIMULIA\CAE\2024\win_b64\code\bin\SMALauncher.exe'


# Function to create input file from template file (parameterization)
def editFile(fname_in, fname_out, str_replaced):
    """
    Create new file from template by replacing placeholders
    """

    # Open and read template file
    with open(fname_in) as f:
        filetext = f.read()

    # Replace parameters
    for textToSearch, textToReplace in str_replaced:
        # print(f'Replacing: {textToSearch} -> {textToReplace}')
        filetext = filetext.replace(textToSearch, textToReplace)

    # Write new file
    with open(fname_out, 'w') as f2:
        f2.write(filetext)
    
    return


# Function to run FEA mesh convergence study
def run_mesh_convergence(jobname, elem_size, template_file, wdir, tdir):
    """
    Run mesh convergence study in Abaqus
    """

    # Job name
    input_file = jobname + '.inp' #Input file generated

    # Parametric mesh
    mesh_file = 'mesh_' + jobname
    rectangle_mesh(mesh_name=mesh_file, elem_size=elem_size)
    with open(mesh_file + '.inp', 'r') as fmesh:
        mesh_lines = fmesh.readlines()

    mesh_lines = mesh_lines[2:] # To skip the first 2 lines
    mesh_string = ''.join(mesh_lines)
    mesh_string = mesh_string.replace('CPS4','CPS4R') # To replace the elem type created by gmsh

    #Update assembly section in input file
    assembly_sets = ''
    for i, line in enumerate(mesh_lines):
        if line.startswith('*NSET'):
            set_lines = [line]
            j = i + 1
            while j < len(mesh_lines) and not mesh_lines[j].startswith('*'):
                set_lines.append(mesh_lines[j])
                j += 1
            # Update NSET line to include instance
            set_lines[0] = set_lines[0].replace('*NSET', '*NSET, instance=Beam-1')
            assembly_sets += ''.join(set_lines) + '\n'


    
    # Parameters pairs [(placeholder, parameter),]
    str_template = [('<BEAM_MESH>', mesh_string),
                    ('<ASSEMBLY_SETS>', assembly_sets),
                    ('<JOBNAME>', jobname)
                    ]


    # Replace strings in template file and generate new input file
    editFile(template_file, input_file, str_template)

    # Copy input file to auxiliary directory
    src = os.path.join(wdir, input_file)         # r'D:\training\Session_2\buckling_01.ans'
    dst = os.path.join(tdir, input_file)  # r'D:\training\Session_2\aux\buckling_01.ans'
    shutil.copyfile(src, dst)

    # Set auxiliary directory as current directory
    os.chdir(tdir)

    #################################################################################

    # Run simulation (call the solver from the cmd)

    run_cmd = [ABQ_CMD, 
                'int', 
                'ask=off', 
                f'job={input_file}']
    
    subprocess.run(run_cmd, shell=True)


    # Back to wdir
    os.chdir(wdir)

    return


def postprocess_mesh_convergence(sta_file):
    """
    Postprocessing - extracting UY
    """
    uy = None

    with open(sta_file, 'r') as file:
        for line in file:
            print(line.strip())  # See what you're parsing
            parts = line.strip().split()
            # Check if this looks like a result row with a float in the last column
            if len(parts) == 10: # Table rows typically have 10 columns. Might need update
                try:
                    val = float(parts[-1]) # Attempt to convert last column
                    print("UY = ", val)
                    uy = val # Save it
                except ValueError:
                    continue
    return uy
