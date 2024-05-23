import os
from PIL import Image
import numpy as np

def convert_image_to_vhdl(image_path, output_path, constant_name):
    """
    Convert an image to a VHDL file.

    Args:
        image_path (str): The path to the input image.
        output_path (str): The path to the output VHDL file.
        constant_name (str): The name of the constant in the VHDL file.
    """
    try:
        # Open the image and ensure it is in RGB mode
        image = Image.open(image_path).convert('RGB')
        data = np.array(image)

        # Get the dimensions of the image
        rows, cols, _ = data.shape

        # Prepare VHDL data lines
        vhdl_data = []
        for row in data:
            vhdl_row = []
            for pixel in row:
                r, g, b = pixel // 16  # Scale down to 4 bits
                vhdl_pixel = (r << 8) | (g << 4) | b
                vhdl_row.append(f"X\"{vhdl_pixel:03X}\"")
            vhdl_data.append("    (" + ", ".join(vhdl_row) + ")")

        # Write to the VHDL file
        with open(output_path, 'w') as f:
            f.write("library ieee;\n")
            f.write("use ieee.std_logic_1164.all;\n\n")
            f.write(f"package {constant_name.lower()}_graphic is\n")
            f.write(f"    constant {constant_name.lower()}_width : integer := {cols};\n")
            f.write(f"    constant {constant_name.lower()}_height : integer := {rows};\n")
            f.write(f"    type {constant_name.lower()}_array is array (0 to {constant_name.lower()}_height-1, 0 to {constant_name.lower()}_width-1) "
                    "of std_logic_vector(11 downto 0);\n")
            f.write(f"    constant {constant_name}_IMAGE : {constant_name.lower()}_array := (\n")
            f.write(",\n".join(vhdl_data) + "\n")
            f.write("    );\n")
            f.write(f"end package {constant_name.lower()}_graphic;\n")
        
        print(f"Successfully converted {image_path} to {output_path}")

    except Exception as e:
        print(f"Error converting {image_path} to VHDL: {e}")

def main():
    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Input and output directories
    input_dir = os.path.join(script_dir, 'original')
    output_dir = os.path.join(script_dir, 'VHDL')

    # Ensure the input directory exists
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    # Ensure the output directory exists, create if not
    os.makedirs(output_dir, exist_ok=True)

    # Convert each PNG file in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith('.png'):
            input_path = os.path.join(input_dir, file_name)
            constant_name = os.path.splitext(file_name)[0].upper()
            output_path = os.path.join(output_dir, f"{constant_name.lower()}_graphic.vhd")
            convert_image_to_vhdl(input_path, output_path, constant_name)

if __name__ == '__main__':
    main()