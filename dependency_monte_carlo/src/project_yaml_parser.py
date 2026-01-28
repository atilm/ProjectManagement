import yaml
from dependency_monte_carlo.src.project import Project, WorkPackage, Estimation

class ProjectYamlParser:
    @staticmethod
    def parse(file_obj) -> Project:
        data = yaml.safe_load(file_obj)
        project_data = data.get('project', {})
        project = Project()
        project.name = project_data.get('name', '')
        for wp_data in project_data.get('work_packages', []):
            wp = WorkPackage()
            wp.id = wp_data.get('id', '')
            wp.name = wp_data.get('name', '')
            wp.description = wp_data.get('description', '')
            wp.dependencies = wp_data.get('depends_on', [])
            est_data = wp_data.get('estimation', {})
            wp.estimation = Estimation(
                min_val=est_data.get('min', 0.0),
                mode=est_data.get('mode', 0.0),
                max_val=est_data.get('max', 0.0)
            )
            project.work_packages.append(wp)
        return project
