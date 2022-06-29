from google.oauth2 import service_account
from googleapiclient import discovery
import google.auth
from google.cloud import container_v1beta1, container_v1
from pprint import pprint
import argparse, sys, time

location = "europe-west4"
cluster_id = "cluster-1"
test = container_v1.ClusterUpdate(desired_node_version="-")


credentials, project_id = google.auth.default()

def list_node_pools():
    client = container_v1.ClusterManagerClient()
    parent = 'projects/{}/locations/{}/clusters/{}'.format(project_id, location, cluster_id)
    request = container_v1.ListNodePoolsRequest(
        parent = parent
    )
    response = client.list_node_pools(request=request)
    return response.node_pools

np_list = list_node_pools()

def list_clusters(project_id: str, location: str) -> None:
    client = container_v1.ClusterManagerClient()
    cluster_location = client.common_location_path(project_id, location)
    request = {"parent": cluster_location}
    list_response = client.list_clusters(request)

    print(
        f"There were {len(list_response.clusters)} clusters in {location} for project {project_id}."
    )
    for cluster in list_response.clusters:
        print(f"- {cluster.name}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("zone", help="GKE Cluster zone")
    args = parser.parse_args()

    if len(sys.argv) != 3:
        parser.print_usage()
        sys.exit(1)

    list_clusters(args.project_id, args.zone)

def update_master(): #update control plane ==============================
    client = container_v1.ClusterManagerClient()
    request = container_v1.UpdateMasterRequest(
        master_version="latest",
        name = 'projects/{}/locations/{}/clusters/{}'.format(project_id, location, cluster_id)
    )

    response = client.update_master(request=request)
    print(response)

update_master()

#========================================================================================

update_pending = True
while update_pending:
    time.sleep(1)
    client = container_v1.ClusterManagerClient()
    get_cluster_request = container_v1.GetClusterRequest(
        name = 'projects/{}/locations/{}/clusters/{}'.format(project_id, location, cluster_id),
    )

    if client.get_cluster(request = get_cluster_request).status == 3:
        update_pending = True
        print('Update still pending, waiting for update to finish')
    else:
        update_pending = False
print('Control plane updated, updating node-pools')


def update_cluster(): #Update the whole cluster with nodes?
    client = container_v1.ClusterManagerClient()
    request = container_v1.UpdateClusterRequest(
        name = 'projects/{}/locations/{}/clusters/{}'.format(project_id, location, cluster_id),
        update = test
    )

    response = client.update_cluster(request=request)
    print(response)

update_cluster()

#====================================


def update_node_pool():
    for np in list_node_pools():
        print(f"Upgrading node pool: {np.name}")
        client = container_v1.ClusterManagerClient()
        request = container_v1.UpdateNodePoolRequest(
            node_version="-",
            image_type="cos_containerd",
            name = 'projects/{}/locations/{}/clusters/{}/nodePools/{}'.format(project_id, location, cluster_id, np.name)
    )
        response = client.update_node_pool(request=request)
        cluster_update_pending = True  #how to check if the nodes are updated????
        while cluster_update_pending:
            time.sleep(1)
            client = container_v1.ClusterManagerClient()
            get_cluster_request = container_v1.GetNodePoolRequest(
                name = 'projects/{}/locations/{}/clusters/{}/nodePools/{}'.format(project_id, location, cluster_id, np.name),
            )
            if client.get_node_pool(request = get_cluster_request).status == 3:
                cluster_update_pending = True
                print('Cluster update still in progress')
            else:
                cluster_update_pending = False
        print('Cluster updated')
        return response

update_node_pool()
#import pdb; pdb.set_trace()


#Credentials saved to file: [/Users/Marinadin.Grin/.config/gcloud/application_default_credentials.json]
