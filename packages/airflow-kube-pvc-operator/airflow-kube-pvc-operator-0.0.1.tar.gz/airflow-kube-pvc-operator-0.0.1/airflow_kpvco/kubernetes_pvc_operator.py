from airflow_kbo import KubernetesBaseOperator

class KubernetesPVCOperator(KubernetesBaseOperator):
    """
    Opinionated operator for kubernetes PVC type management.
    Only allow client to pass in yaml files
    """

    def __init__( self, **kwargs):
        super().__init__(**kwargs)


    def execute(self, context):
        ...