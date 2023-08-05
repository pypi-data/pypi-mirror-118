# Airflow Kubernetes PVC Operator
Airflow operator for kubernetes PVC type


Aspirations:

- make an operator to take in a yaml file describing a pvc object and have airflow manage its life cycle
- should be able to plug in with kube job operator
- would be cool to modify the UI to show the pvc is bound to the Job
- throw a warning if resource quota for storage limit in namespace is not set, Airflow should help onboard people to kube 'best practices'


## Notes

Not to be used yet