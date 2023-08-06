import pandas as pd

def generate_centroids(model):
    cluster_center = model.cluster_centers_
    for i in range(0, cluster_center.shape[0]):
        chargable_weight_centroids = pd.DataFrame(
            {'cluster': list(set(model.labels_)),
             'dcp15_centroid': [cluster_center[i, 2] for i in range(0, cluster_center.shape[0])],
             'dcp14_centroid': [cluster_center[i, 3] for i in range(0, cluster_center.shape[0])],
             'dcp13_centroid': [cluster_center[i, 4] for i in range(0, cluster_center.shape[0])],
             'dcp12_centroid': [cluster_center[i, 5] for i in range(0, cluster_center.shape[0])],
             'dcp11_centroid': [cluster_center[i, 6] for i in range(0, cluster_center.shape[0])],
             'dcp10_centroid': [cluster_center[i, 7] for i in range(0, cluster_center.shape[0])],
             'dcp9_centroid': [cluster_center[i, 8] for i in range(0, cluster_center.shape[0])],
             'dcp8_centroid': [cluster_center[i, 9] for i in range(0, cluster_center.shape[0])],
             'dcp7_centroid': [cluster_center[i, 10] for i in range(0, cluster_center.shape[0])],
             'dcp6_centroid': [cluster_center[i, 11] for i in range(0, cluster_center.shape[0])],
             'dcp5_centroid': [cluster_center[i, 12] for i in range(0, cluster_center.shape[0])],
             'dcp4_centroid': [cluster_center[i, 13] for i in range(0, cluster_center.shape[0])],
             'dcp3_centroid': [cluster_center[i, 14] for i in range(0, cluster_center.shape[0])],
             'dcp2_centroid': [cluster_center[i, 15] for i in range(0, cluster_center.shape[0])],
             'dcp1_centroid': [cluster_center[i, 16] for i in range(0, cluster_center.shape[0])],
             'dcp0_centroid': [cluster_center[i, 17] for i in range(0, cluster_center.shape[0])],
             })
    return chargable_weight_centroids


def generate_kproto_centroids(model):
    cluster_center = model.cluster_centroids_
    for i in range(0, cluster_center.shape[0]):
        chargable_weight_centroids = pd.DataFrame(
            {'cluster': list(set(model.labels_)),
             'dcp15_centroid': [cluster_center[i, 2] for i in range(0, cluster_center.shape[0])],
             'dcp14_centroid': [cluster_center[i, 3] for i in range(0, cluster_center.shape[0])],
             'dcp13_centroid': [cluster_center[i, 4] for i in range(0, cluster_center.shape[0])],
             'dcp12_centroid': [cluster_center[i, 5] for i in range(0, cluster_center.shape[0])],
             'dcp11_centroid': [cluster_center[i, 6] for i in range(0, cluster_center.shape[0])],
             'dcp10_centroid': [cluster_center[i, 7] for i in range(0, cluster_center.shape[0])],
             'dcp9_centroid': [cluster_center[i, 8] for i in range(0, cluster_center.shape[0])],
             'dcp8_centroid': [cluster_center[i, 9] for i in range(0, cluster_center.shape[0])],
             'dcp7_centroid': [cluster_center[i, 10] for i in range(0, cluster_center.shape[0])],
             'dcp6_centroid': [cluster_center[i, 11] for i in range(0, cluster_center.shape[0])],
             'dcp5_centroid': [cluster_center[i, 12] for i in range(0, cluster_center.shape[0])],
             'dcp4_centroid': [cluster_center[i, 13] for i in range(0, cluster_center.shape[0])],
             'dcp3_centroid': [cluster_center[i, 14] for i in range(0, cluster_center.shape[0])],
             'dcp2_centroid': [cluster_center[i, 15] for i in range(0, cluster_center.shape[0])],
             'dcp1_centroid': [cluster_center[i, 16] for i in range(0, cluster_center.shape[0])],
             'dcp0_centroid': [cluster_center[i, 17] for i in range(0, cluster_center.shape[0])],
             })
    return chargable_weight_centroids


def generate_tskmeans_centroids(model):
    cluster_center = model.cluster_centers_
    for i in range(0, cluster_center.shape[0]):
        chargable_weight_centroids = pd.DataFrame(
            {'cluster': list(set(model.labels_)),
             'dcp15_centroid': [cluster_center[i, 2][0] for i in range(0, cluster_center.shape[0])],
             'dcp14_centroid': [cluster_center[i, 3][0] for i in range(0, cluster_center.shape[0])],
             'dcp13_centroid': [cluster_center[i, 4][0] for i in range(0, cluster_center.shape[0])],
             'dcp12_centroid': [cluster_center[i, 5][0] for i in range(0, cluster_center.shape[0])],
             'dcp11_centroid': [cluster_center[i, 6][0] for i in range(0, cluster_center.shape[0])],
             'dcp10_centroid': [cluster_center[i, 7][0] for i in range(0, cluster_center.shape[0])],
             'dcp9_centroid': [cluster_center[i, 8][0] for i in range(0, cluster_center.shape[0])],
             'dcp8_centroid': [cluster_center[i, 9][0] for i in range(0, cluster_center.shape[0])],
             'dcp7_centroid': [cluster_center[i, 10][0] for i in range(0, cluster_center.shape[0])],
             'dcp6_centroid': [cluster_center[i, 11][0] for i in range(0, cluster_center.shape[0])],
             'dcp5_centroid': [cluster_center[i, 12][0] for i in range(0, cluster_center.shape[0])],
             'dcp4_centroid': [cluster_center[i, 13][0] for i in range(0, cluster_center.shape[0])],
             'dcp3_centroid': [cluster_center[i, 14][0] for i in range(0, cluster_center.shape[0])],
             'dcp2_centroid': [cluster_center[i, 15][0] for i in range(0, cluster_center.shape[0])],
             'dcp1_centroid': [cluster_center[i, 16][0] for i in range(0, cluster_center.shape[0])],
             'dcp0_centroid': [cluster_center[i, 17][0] for i in range(0, cluster_center.shape[0])],
             })
    return chargable_weight_centroids


def generate_dcp_centroids(model, dcp):
    cluster_center = model.cluster_centers_
    cluster_name = 'dcp_'+str(dcp)+'_cluster'
    centroid_name = 'dcp_x_'+str(dcp)+'_centroid'
    chargable_weight_centroids = pd.DataFrame(
        {cluster_name: list(set(model.labels_)),
         centroid_name: [cluster_center[i, 2]
                         for i in range(0, cluster_center.shape[0])]
         })
    return chargable_weight_centroids
