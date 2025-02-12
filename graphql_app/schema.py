import graphene
from graphene_django.types import DjangoObjectType
from .models import Client, Project, Employee, EmployeeProjectAssignment
from graphene_file_upload.scalars import Upload

# Define Client Type
class ClientType(DjangoObjectType):
    class Meta:
        model = Client
        fields = "__all__"

# Define Project Type
class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = "__all__"

# Define Employee Type
class EmployeeType(DjangoObjectType):
    assigned_projects = graphene.List(ProjectType)
    class Meta:
        model = Employee
        fields = "__all__"
        
    def resolve_assigned_projects(self, info):
        return self.assigned_projects.all()
        
class EmployeeProjectAssignmentType(DjangoObjectType):
    class Meta:
        model = EmployeeProjectAssignment
        fields = "__all__"

# Query Class
class Query(graphene.ObjectType):
    all_clients = graphene.List(ClientType)
    all_projects = graphene.List(ProjectType)
    all_employees = graphene.List(EmployeeType)
    all_employee_project_assignments = graphene.List(EmployeeProjectAssignmentType)
    employee_detail = graphene.Field(EmployeeType, id=graphene.ID())
    
    def resolve_all_clients(self, info):
        return Client.objects.all()
    
    def resolve_all_projects(self, info):
        return Project.objects.all()
    
    def resolve_all_employees(self, info):
        return Employee.objects.all()
    
    def resolve_all_employee_project_assignments(self, info):
        return EmployeeProjectAssignment.objects.all()
    
    def resolve_employee_detail(self, info, id):
        try:
            return Employee.objects.get(pk=id)
        except Employee.DoesNotExist:
            return None

# Create Mutations for CRUD operations
class CreateClient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        contact_number = graphene.String(required=True)
        email = graphene.String(required=True)

    client = graphene.Field(ClientType)

    def mutate(self, info, name, contact_number, email):
        client = Client(name=name, contact_number=contact_number, email=email)
        client.save()
        return CreateClient(client=client)

class UpdateClient(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        contact_number = graphene.String()
        email = graphene.String()

    client = graphene.Field(ClientType)

    def mutate(self, info, id, name=None, contact_number=None, email=None):
        client = Client.objects.get(pk=id)
        if name:
            client.name = name
        if contact_number:
            client.contact_number = contact_number
        if email:
            client.email = email
        client.save()
        return UpdateClient(client=client)

class DeleteClient(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        client = Client.objects.get(pk=id)
        client.delete()
        return DeleteClient(success=True)


class CreateProject(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        client_id = graphene.Int(required=True)
        price_type = graphene.String(required=True)
        price = graphene.Float(required=True)
        file = Upload(required=True)
        delivery_date = graphene.Date(required=True)
        status = graphene.String()

    project = graphene.Field(ProjectType)

    def mutate(self, info, name, client_id, price_type, price, file, delivery_date, status="pending"):
        client = Client.objects.get(pk=client_id)
        project = Project(name=name, client=client, price_type=price_type, price=price, file=file, delivery_date=delivery_date, status=status)
        project.save()
        return CreateProject(project=project)
    
class UpdateProject(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        client_id = graphene.Int()
        price_type = graphene.String()
        price = graphene.Float()
        delivery_date = graphene.Date()
        status = graphene.String()

    project = graphene.Field(ProjectType)

    def mutate(self, info, id, name=None, client_id=None, price_type=None, price=None, delivery_date=None, status=None):        
        project = Project.objects.get(pk=id)
        if name:
            project.name = name
        if client_id:
            project.client = Client.objects.get(pk=client_id)
        if price_type:
            project.price_type = price_type
        if price:
            project.price = price
        if delivery_date:
            project.delivery_date = delivery_date
        if status:
            project.status = status
        project.save()
        return UpdateProject(project=project)

class DeleteProject(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        project = Project.objects.get(pk=id)
        project.delete()
        return DeleteProject(success=True)


class CreateEmployee(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        contact_number = graphene.String(required=True)
        email = graphene.String(required=True)

    employee = graphene.Field(EmployeeType)

    def mutate(self, info, name, contact_number, email):
        employee = Employee(name=name, contact_number=contact_number, email=email)
        employee.save()
        return CreateEmployee(employee=employee)
    
class UpdateEmployee(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        contact_number = graphene.String()
        email = graphene.String()

    employee = graphene.Field(EmployeeType)

    def mutate(self, info, id, name=None, contact_number=None, email=None):
        employee = Employee.objects.get(pk=id)
        if name:
            employee.name = name
        if contact_number:
            employee.contact_number = contact_number
        if email:
            employee.email = email
        employee.save()
        return UpdateEmployee(employee=employee)

class DeleteEmployee(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        employee = Employee.objects.get(pk=id)
        employee.delete()
        return DeleteEmployee(success=True)

class CreateAssignEmployeeToProject(graphene.Mutation):
    class Arguments:
        employee_id = graphene.Int(required=True)
        project_id = graphene.Int(required=True)
        start_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)

    employee_project_assignment = graphene.Field(EmployeeProjectAssignmentType)

    def mutate(self, info, employee_id, project_id, start_date, end_date):
        employee = Employee.objects.get(pk=employee_id)
        project = Project.objects.get(pk=project_id)
        assignment = EmployeeProjectAssignment(employee=employee, project=project, start_date=start_date, end_date=end_date)
        assignment.save()
        return CreateAssignEmployeeToProject(employee_project_assignment=assignment)
    
class UpdateAssignEmployeeToProject(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        employee_id = graphene.Int()
        project_id = graphene.Int()
        start_date = graphene.Date()
        end_date = graphene.Date()

    employee_project_assignment = graphene.Field(EmployeeProjectAssignmentType)

    def mutate(self, info, id, employee_id=None, project_id=None, start_date=None, end_date=None):
        assignment = EmployeeProjectAssignment.objects.get(pk=id)
        if employee_id:
            assignment.employee_id = employee_id
        if project_id:
            assignment.project_id = project_id
        if start_date:
            assignment.start_date = start_date
        if end_date:
            assignment.end_date = end_date
        assignment.save()
        return UpdateAssignEmployeeToProject(employee_project_assignment=assignment)

class DeleteAssignEmployeeToProject(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        assignment = EmployeeProjectAssignment.objects.get(pk=id)
        assignment.delete()
        return DeleteAssignEmployeeToProject(success=True)
    
class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()
    update_client = UpdateClient.Field()
    delete_client = DeleteClient.Field()
    
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()

    create_assign_employee_to_project = CreateAssignEmployeeToProject.Field()
    update_assign_employee_to_project = UpdateAssignEmployeeToProject.Field()
    delete_assign_employee_to_project = DeleteAssignEmployeeToProject.Field()

# Define the Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
