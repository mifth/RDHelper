RDHelper is an extension for the RenderDoc application which helps to inspect meshes and textures.
RenderDoc: https://github.com/baldurk/renderdoc

Features:
- Get all or only unique textures.
- Get all or only unique meshes.
- Sort meshes by an amount of triangles.
- Sort textures by size.
- Limit an amount of Event IDs by setting StartEID and EndEID values.
- Export selected meshes to an OBJ file (no UVs and VertexColors).

![image](https://github.com/user-attachments/assets/0875f2d4-bfd5-4c91-8583-299d9a010095)
![image](https://github.com/user-attachments/assets/3168de68-ed3c-4b0b-a194-c93ec37d0982)

UE5 Nanite meshes aren't supported.

Installation:
- Open the Extension Manager. Tools->ManageExtensions.
- Press the OpenLocation button in the Extension Manager. 
- Copy the content of the repository as a folder to RenderDoc's extensions folder. On Windows it will be at C:\Users\MyUser\AppData\Roaming\qrenderdoc\extensions\RDHelper.
- Open the RDHelper window with Window->RDHelperWindow.

![image](https://github.com/user-attachments/assets/e41ab70e-81a0-4476-9373-cec2833e580f)

