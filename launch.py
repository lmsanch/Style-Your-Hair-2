import gradio as gr
import subprocess
import sys
import os

import gradio as gr
import subprocess
import sys
import os

def style_your_hair(im_path1, im_path2, save_all, embedding_dir, sign, size, ckpt, device, learning_rate):
    try:
        fixed_output_dir = "./image_output/"
        # Construct the command with the provided arguments
        save_all_flag = "--save_all" if save_all else ""
        # command = f"python main.py --input_dir ./ --im_path1 {im_path1} --im_path2 {im_path2} {save_all_flag} --embedding_dir {embedding_dir} --sign {sign} --size {size} --ckpt {ckpt} --device {device} --learning_rate {learning_rate} --output_dir {output_dir}"
        command = f"python main.py --input_dir ./ --im_path1 {im_path1} --im_path2 {im_path2} {save_all_flag} --embedding_dir {embedding_dir} --sign {sign} --size {size} --ckpt {ckpt} --device {device} --learning_rate {learning_rate} --output_dir {fixed_output_dir} --warp_loss_with_prev_list delta_w style_hair_slic_large --version final"
        # Print the command for debugging
        print("Executing command:", command)

        # Execute the command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Print stdout and stderr for debugging
        print("Standard Output:", process.stdout)
        print("Standard Error:", process.stderr)

        # Check for errors
        if process.returncode != 0:
            return None, f"Error: {process.stderr}"

        # Print contents of the output directory for debugging
        print(f"Contents of '{fixed_output_dir}':", os.listdir(fixed_output_dir))

        # Find the output image in the specified output directory
        for file in os.listdir(fixed_output_dir):
            if file.endswith(".png"):
                output_image_path = os.path.join(fixed_output_dir, file)
                return output_image_path, "Process completed successfully."

        return None, "Output image not found."

    except Exception as e:
        print("Exception occurred:", str(e))
        return None, str(e)
# Define the Gradio interface
iface = gr.Interface(
    fn=style_your_hair,
    inputs=[
        gr.components.Image(type="filepath", label="Input Image"),
        gr.components.Image(type="filepath", label="Target Image"),
        gr.components.Checkbox(label="Save All", value=True),
        gr.components.Textbox(label="Embedding Directory", value='./output/'),
        gr.components.Radio(label="Sign", choices=["realistic", "fidelity"], value="realistic"),
        gr.components.Slider(minimum=256, maximum=2048, step=256, value=1024, label="Size"),
        gr.components.Textbox(label="Checkpoint", value="pretrained_models/ffhq.pt"),
        gr.components.Radio(label="Device", choices=["cuda"], value="cuda"),
        gr.components.Slider(minimum=0.001, maximum=0.1, step=0.001, value=0.01, label="Learning Rate"),
    ],
    outputs=[
        gr.components.Image(label="Processed Image"),
        gr.components.Text(label="Console Output")
    ]
)

iface.launch()
'''
python main.py --save_all \
    --version final \
    --flip_check \
    --input_dir ./ffhq_image/ \
    --im_path1 61663.png \
    --im_path2 57895.png \
    --output_dir ./image_output/ \
    --warp_loss_with_prev_list delta_w style_hair_slic_large
'''
