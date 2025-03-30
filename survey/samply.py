import os

def combine_tree_files(folder_path, n, output_file='Combined_Trees.html'):
    combined_content = ""

    for i in range(1, n + 1):
        filename = f"Tree_{i}.html"
        file_path = os.path.join(folder_path, filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                combined_content += f"\n<!-- Start of {filename} -->\n"
                combined_content += content
                combined_content += f"\n<!-- End of {filename} -->\n"
        except FileNotFoundError:
            print(f"Warning: {filename} not found, skipping.")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_content)

    print(f"Combined content written to '{output_file}'")


combine_tree_files(folder_path=r'.\Trees', n=17)
