# Remove old build and log folder
rm -r -f pbs_output
rm -r -f bld

# Make new folder structure
sed '/^$/d;s/ /\//g' ./parameters/bld_folder_structure.txt | xargs mkdir -p