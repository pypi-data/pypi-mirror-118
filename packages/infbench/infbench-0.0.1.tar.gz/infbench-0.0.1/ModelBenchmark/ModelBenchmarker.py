from openvino.inference_engine import IECore, StatusCode
import argparse
import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    """Parse and return command line arguments"""
    parser = argparse.ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    # fmt: off
    args.add_argument('-h', '--help', action='help', help='Show this help message and exit.')
    args.add_argument('-m', '--model', required=True, type=str,
                      help='Required. Path to an .xml or .onnx file with a trained model.')
    args.add_argument('-i', '--input', required=True, type=str, nargs='+', help='Required. Path to an image file(s).')
    args.add_argument('-l', '--extension', type=str, default=None,
                      help='Optional. Required by the CPU Plugin for executing the custom operation on a CPU. '
                           'Absolute path to a shared library with the kernels implementations.')
    args.add_argument('-c', '--config', type=str, default=None,
                      help='Optional. Required by GPU or VPU Plugins for the custom operation kernel. '
                           'Absolute path to operation description file (.xml).')
    args.add_argument('-d', '--device', default='CPU', type=str,
                      help='Optional. Specify the target device to infer on; CPU, GPU, MYRIAD, HDDL or HETERO: '
                           'is acceptable. The sample will look for a suitable plugin for device specified. '
                           'Default value is CPU.')
    args.add_argument('--labels', default=None, type=str, help='Optional. Path to a labels mapping file.')
    args.add_argument('-nt', '--number_top', default=10, type=int, help='Optional. Number of top results.')
    # fmt: on
    return parser.parse_args()


class InferenceBenchmarker:

    def __init__(self, args):
        self.ie = IECore()
        self.net = ie.read_network(model=args.model)
        self.input = args.input
        self.device_name = args.device
        self.__configure()

    def __configure(self):
        self.net.input_info[input_blob].precision = 'U8'
        self.net.ouputs[out_blob].precision = 'FP32'
        self.num_of_input = len(self.input)
        self.num_of_classes = len(self.net.outputs[out_blob].shape)

    def __load_model_to_device(self):
        self.exec_net = self.ie.load_network(network=self.net)

ie = IECore()
net = ie.read_network(model=args.model)

# Get names of input and output blobs
input_blob = next(iter(net.input_info))
out_blob = next(iter(net.outputs))

# Set input and output precision manually
net.input_info[input_blob].precision = 'U8'
net.outputs[out_blob].precision = 'FP32'

# Get a number of input images
num_of_input = len(args.input)

# Get a number of classes recognized by a model
num_of_classes = max(net.outputs[out_blob].shape)

# Loading model to device
exec_net = ie.load_network(network=net, device_name=args.device, num_requests=num_of_input)

input_data = []
_, _, h, w = net.input_info[input_blob].input_data.shape

for i in range(num_of_input):
    image = cv2.imread(args.input[i])

    if image.shape[:-1] != (h, w):
        image = cv2.resize(image, (w, h))

    # Change data layout from HWC to CHW
    image = image.transpose((2, 0, 1))
    # Add N dimension to transform to NCHW
    image = np.expand_dims(image, axis=0)

    input_data.append(image)

# Do inference
for i in range(num_of_input):
    exec_net.requests[i].async_infer({input_blob: input_data[i]})

# Create a list to control a order of output
output_queue = list(range(num_of_input))

while True:
    for i in output_queue:
        # Immediately returns a inference status without blocking or interrupting
        infer_status = exec_net.requests[i].wait(0)

        if infer_status == StatusCode.RESULT_NOT_READY:
            continue

        if infer_status != StatusCode.OK:
            print('Infer status different than "StatusCode.OK" at ' + i + '.')

        # Read infer request results from buffer
        res = exec_net.requests[i].output_blobs[out_blob].buffer

        # Change a shape of a numpy.ndarray with results to get another one with one dimension
        probs = res.reshape(num_of_classes)

        # Get an array of args.number_top class IDs in descending order of probability
        top_n_indexes = np.argsort(probs)[-args.number_top:][::-1]

        header = 'classid probability'
        header = header + ' label' if args.labels else header

        for class_id in top_n_indexes:
            probability_indent = ' ' * (len('classid') - len(str(class_id)) + 1)
            label_indent = ' ' * (len('probability') - 8) if args.labels else ''

        output_queue.remove(i)

    if len(output_queue) == 0:
        break
