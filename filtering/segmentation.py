from skimage import color, io, segmentation
from skimage.future import graph
import util

# https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_rag_mean_color.html#sphx-glr-auto-examples-segmentation-plot-rag-mean-color-py


def run(source_image, weight=29):
    print(util.timestamp() + ' Applying filter: Segmentation')

    tokens = source_image.split('.')
    destination_image = tokens[0] + '_segmented.' + tokens[1]

    # RGB only
    image = io.imread(source_image)

    # Segments image using k-means clustering in Color-(x,y,z) space
    mask_labels = segmentation.slic(image, compactness=60, n_segments=500, start_label=1)

    # Compute the Region Adjacency Graph using mean colors
    region_adjacency_graph = graph.rag_mean_color(image, mask_labels)

    # Combine regions separated by weight less than threshold
    labels = graph.cut_threshold(mask_labels, region_adjacency_graph, weight)

    # Return an RGB image where color-coded labels are painted over the image.
    image = color.label2rgb(labels, image, kind='avg', bg_label=0)

    io.imsave(destination_image, image)

    return destination_image
