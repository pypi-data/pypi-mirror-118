from string import Template
from .DeploymentController import DeploymentController
from .DescriptionGenerator import CreateDepl


class DeplManager:
    def __init__(self):
        self.depl_controller = DeploymentController.DeplController()

        self.ids = {}
        self.id_counter = 0

        self.deployments = {}

    # deployments is and array of deployments dictionary { deployment: deployment, d_type:d_type }
    def save_depoyment(self, deployments, depl_id, d_type):
        self.deployments[depl_id] = {
            'deployments': deployments,
            'd_type': d_type
        }

    def delete_deployment(self, depl_id):
        self.deployments.pop(depl_id)

    def instantiate_with_id(self, id):
        depls = self.deployments[id]

        for depl in depls:
            id = self.get_new_id(depl.d_type)
            if depl.d_type == 'pod':
                depl.deployment["depl_name"] = Template(depl.deployment["depl_name"]).substitute(id=id)

            if depl.d_type == 'service':
                pass
        # names, depl_settings, svc_settings, svc_np_settings = self.create_drone(id)
        # self.ids[id] = names

        # self.depl_controller.create_depl(depl_settings)
        # self.depl_controller.create_svc(svc_settings)
        # self.depl_controller.create_svc(svc_np_settings)

        return id

    def delete_instance_with_id(self, id):
        if int(id) in self.ids:
            names = self.ids[int(id)]
            self.depl_controller.delete_depl(names[0])
            self.depl_controller.delete_svc(names[1])
            self.depl_controller.delete_svc(names[2])
            return 1
        else:
            return -1

    def get_new_id(self, d_type):
        self.id_counter += 1
        return self.id_counter

    # test deployment
    def create_drone(self, id):
        depl_name = Template("drone-$id").substitute(id=id)
        svc_name = Template("drone-svc-$id").substitute(id=id)
        container_name = Template("drone-c-$id").substitute(id=id)
        np_svc_name = Template("drone-svc-np-$id").substitute(id=id)

        depl_settings = {
            "depl_name": depl_name,
            "container_name": container_name,
            "image": "luciantin/virtual-drone",
            "label": {'app': container_name},
            "container_port": 80,
            "command": None,
        }

        svc_settings = {
            "svc_name": svc_name,
            "type": "ClusterIP",
            "label": {'svc': svc_name},
            "selector": {'app': container_name},
            "ports": [[5000, 5000]]
        }

        svc_np_settings = {
            "svc_name": np_svc_name,
            "type": "NodePort",
            "label": None,
            "selector": {'app': container_name},
            "ports": [[5000, 5000]]
        }
        names = [depl_name, svc_name, np_svc_name]
        return names, CreateDepl.CreatePod(depl_settings), CreateDepl.CreateService(svc_settings), CreateDepl.CreateService(svc_np_settings)
