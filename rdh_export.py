import renderdoc as rd
import qrenderdoc as qrd

# We'll need the struct data to read out of bytes objects
import struct

# We base our data on a MeshFormat, but we add some properties
class MeshData(rd.MeshFormat):
	indexOffset = 0
	name = ''

# Get a list of MeshData objects describing the vertex outputs at this draw
def GetMeshOutputs(controller, postvs):
    meshOutputs = []
    posidx = 0

    vs = controller.GetPipelineState().GetShaderReflection(rd.ShaderStage.Vertex)

	# Repeat the process, but this time sourcing the data from postvs.
	# Since these are outputs, we iterate over the list of outputs from the
	# vertex shader's reflection data
    for attr in vs.outputSignature:
        # Copy most properties from the postvs struct
        meshOutput = MeshData()
        meshOutput.indexResourceId = postvs.indexResourceId
        meshOutput.indexByteOffset = postvs.indexByteOffset
        meshOutput.indexByteStride = postvs.indexByteStride
        meshOutput.baseVertex = postvs.baseVertex
        meshOutput.indexOffset = 0
        meshOutput.numIndices = postvs.numIndices

        # The total offset is the attribute offset from the base of the vertex,
        # as calculated by the stride per index
        meshOutput.vertexByteOffset = postvs.vertexByteOffset
        meshOutput.vertexResourceId = postvs.vertexResourceId
        meshOutput.vertexByteStride = postvs.vertexByteStride

        # Construct a resource format for this element
        meshOutput.format = rd.ResourceFormat()
        meshOutput.format.compByteWidth = rd.VarTypeByteSize(attr.varType)
        meshOutput.format.compCount = attr.compCount
        meshOutput.format.compType = rd.VarTypeCompType(attr.varType)
        meshOutput.format.type = rd.ResourceFormatType.Regular

        meshOutput.name = attr.semanticIdxName if attr.varName == '' else attr.varName

        if attr.systemValue == rd.ShaderBuiltin.Position:
            posidx = len(meshOutputs)

        meshOutputs.append(meshOutput)

    # Shuffle the position element to the front
    if posidx > 0:
        pos = meshOutputs[posidx]
        del meshOutputs[posidx]
        meshOutputs.insert(0, pos)

    accumOffset = postvs.vertexByteOffset

    for i in range(0, len(meshOutputs)):
        meshOutputs[i].vertexByteOffset = accumOffset

        # Note that some APIs such as Vulkan will pad the size of the attribute here
        # while others will tightly pack
        fmt = meshOutputs[i].format

        accumOffset += (8 if fmt.compByteWidth > 4 else 4) * fmt.compCount

    return meshOutputs

def GetIndices(controller, mesh):
    # Get the character for the width of index
    indexFormat = 'B'
    if mesh.indexByteStride == 2:
        indexFormat = 'H'
    elif mesh.indexByteStride == 4:
        indexFormat = 'I'

    # Duplicate the format by the number of indices
    indexFormat = str(mesh.numIndices) + indexFormat

    # If we have an index buffer
    if mesh.indexResourceId != rd.ResourceId.Null():
        # Fetch the data
        ibdata = controller.GetBufferData(mesh.indexResourceId,
                                          mesh.indexByteOffset, 0)

        # Unpack all the indices, starting from the first index to fetch
        offset = mesh.indexOffset * mesh.indexByteStride
        indices = struct.unpack_from(indexFormat, ibdata, offset)

        # Apply the baseVertex offset
        return [i + mesh.baseVertex for i in indices]
    else:
        # With no index buffer, just generate a range
        return tuple(range(mesh.numIndices))

# Unpack a tuple of the given format, from the data
def UnpackData(fmt, buffer_data: bytes, offset):
    # We don't handle 'special' formats - typically bit-packed such as 10:10:10:2
    if fmt.Special():
        raise RuntimeError("Packed formats are not supported!")

    formatChars = {}
    #                                 012345678
    # formatChars[rd.CompType.UInt] = "xBHxIxxxL"
    # formatChars[rd.CompType.SInt] = "xbhxixxxl"
    formatChars[rd.CompType.Float] = "xxexfxxxd"  # only 2, 4 and 8 are valid

    vertexFormat2 = str(fmt.compCount) + formatChars[fmt.compType][fmt.compByteWidth]
    value = struct.unpack_from(vertexFormat2, buffer_data, offset)

    return value

def ExportToOBJ(r_ctrl: rd.ReplayController, mesh_data, obj_file, vertex_index, indices, buffer_data: bytes):
    tris = []
    tris_data = []

    attr = mesh_data[0]

    # Variant
    # position = list(zip(position[3::4], position[1::4], position[::4]))
    # data = r_ctrl.GetBufferData(attr.vertexResourceId, attr.vertexByteOffset, 0)

    all_indices = mesh_data[0].numIndices
    
    # We'll decode the first three indices making up a triangle
    for i in range(all_indices):
        idx = indices[i]
        offset = attr.vertexByteStride * idx
        # offset = attr.vertexByteOffset + attr.vertexByteStride * idx
        position = UnpackData(attr.format, buffer_data, offset)

        if position:
            # Not sure if we should do (position[2] + position[3]) for the Z value
            verts = (position[0], position[1], position[2] + position[3])
        else:
            verts = (0.0, 0.0, 0.0)

        tris_data.append(i + 1 + vertex_index)

        # Append polygons
        if len(tris_data) == 3:
            tris.append(tris_data)
            tris_data = []

        obj_file.write("v " + ' '.join(str(x) for x in verts) + "\n")

    for triangle in tris:
        obj_file.write("f " + ' '.join(str(x) for x in triangle) + "\n")

    if indices:
        return all_indices
    else:
        return None
