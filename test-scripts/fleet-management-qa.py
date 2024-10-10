import asyncio

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.proto.app import Authorization
from viam.proto.app import AuthorizedPermissions
from viam.proto.app.packages import PackageType
from viam.proto.app import Visibility, RegistryItemStatus
from viam.proto.app import Model, ModuleFileInfo
from viam.app.app_client import APIKeyAuthorization

async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload='<API-KEY>',
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity='<API-KEY-ID>'
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():

    # Make a ViamClient
    viam_client = await connect()
    # Instantiate an AppClient called "cloud"
    # to run fleet management API methods on
    cloud = viam_client.app_client

    # BUG: grpc error
    id = await cloud.get_user_id_by_email("sierra.guequierre@viam.com")
    print(f"USER ID: {id}")

    # BUG: grpc error
    organization = await cloud.create_organization("name")
    print(f"Organization: {organization}")

    org_list = await cloud.list_organizations()
    print(org_list)

    org_list = await cloud.get_organizations_with_access_to_location("<YOUR-LOCATION-ID>")
    print(org_list)

    # BUG: grpc error
    member_list, invite_list = await cloud.list_organization_members(org_id="<YOUR-ORG-ID>")
    first_user_id = member_list[0].user_id
    org_list = await cloud.list_organizations_by_user(first_user_id)
    print(org_list)

    org = await cloud.get_organization("<YOUR-ORG-ID>")
    print(org)

    available = await cloud.get_organization_namespace_availability(
    public_namespace="sierra")
    print(available)

    organization = await cloud.update_organization(
      org_id="<YOUR-ORG-ID>",
      name="C3P0's Org",
      public_namespace="c3p0"
    )
    print(organization)

    await cloud.delete_organization("298d2032-7a63-4a7f-810c-0a841e219bd9")

    member_list, invite_list = await cloud.list_organization_members("<YOUR-ORG-ID>")
    print(f"invite list: {invite_list}, member list: {member_list}")

    await cloud.create_organization_invite("<YOUR-ORG-ID>", "youremail@email.com")

    auth = Authorization(
        authorization_type="role",
        authorization_id="location_owner",
        resource_type="location", # "robot", "location", or "organization"
        # machine id, location id or org id
        resource_id="<YOUR-LOCATION-ID>",
        identity_id="",
        organization_id="<YOUR-ORG-ID>",
        identity_type=""
    )

    update_invite = await cloud.update_organization_invite_authorizations(
        org_id="<YOUR-ORG-ID>",
        email="sguequierre@gmail.com",
        add_authorizations=[auth])

    print(update_invite)

    member_list, invite_list = await cloud.list_organization_members(org_id="<YOUR-ORG-ID>")

    first_user_id = member_list[0].user_id

    await cloud.delete_organization_member(org_id="<YOUR-ORG-ID>", user_id=first_user_id)

    await cloud.delete_organization_invite("<YOUR-ORG-ID>", "c3po@viam.com")

    org_invite = await cloud.resend_organization_invite("<YOUR-ORG-ID>", "bb8@viam.com")
    print(org_invite)

    my_new_location = await cloud.create_location(org_id="<YOUR-ORG-ID>", name="Robotville", parent_location_id="<YOUR-LOCATION-ID>")
    print(my_new_location)

    location = await cloud.get_location(location_id="<YOUR-LOCATION-ID>")
    print(location)

    my_updated_location = await cloud.update_location(
        location_id="<YOUR-LOCATION-ID>",
        name="Robotville 2",
        parent_location_id="<YOUR-LOCATION-ID-PARENT>",
    )
    print(f"my updated location {my_updated_location}")

    await cloud.delete_location(location_id="<YOUR-LOCATION-ID-PARENT>")

    locations = await cloud.list_locations("<YOUR-ORG-ID>")
    print(locations)

    await cloud.share_location("<YOUR-ORG-ID>", "<YOUR-LOCATION-ID>")

    await cloud.unshare_location("<YOUR-ORG-ID>", "<YOUR-LOCATION-ID>")

    loc_auth = await cloud.location_auth(location_id="<YOUR-LOCATION-ID>")
    print(loc_auth)

    new_loc_auth = await cloud.create_location_secret(location_id="<YOUR-LOCATION-ID>")
    print(new_loc_auth)
    # TODO: Get location secret id from new loc auth

    await cloud.delete_location_secret(
        location_id="<YOUR-LOCATION-ID>",
        secret_id="<YOUR-LOCATION-SECRET-ID>")
    
    loc_auth = await cloud.location_auth(location_id="<YOUR-LOCATION-ID>")
    print(loc_auth)
    
    robot = await cloud.get_robot(robot_id="<YOUR-MACHINE-ID>")
    print(robot)

    api_keys = await cloud.get_robot_api_keys(robot_id="<YOUR-MACHINE-ID>")
    print(api_keys)

    list_of_parts = await cloud.get_robot_parts(
        robot_id="<YOUR-MACHINE-ID>"
    )
    print(list_of_parts)

    my_robot_part = await cloud.get_robot_part(
      robot_part_id="<YOUR-PART-ID>")
    print(my_robot_part)

    part_logs = await cloud.get_robot_part_logs(
      robot_part_id="<YOUR-PART-ID>", num_log_entries=20
    )
    print(part_logs)

    logs_stream = await cloud.tail_robot_part_logs(
        robot_part_id="<YOUR-PART-ID>"
    )
    print(logs_stream)

    part_history = await cloud.get_robot_part_history(
        robot_part_id="<YOUR-PART-ID>"
    )
    print(part_history)

    new_part_id = await cloud.new_robot_part(
        robot_id="<YOUR-MACHINE-ID>", part_name="myNewSubPart"
    )
    print(new_part_id)

    await cloud.delete_robot_part(
        robot_part_id="<YOUR-PART-ID-TO-DELETE>"
    )

    await cloud.mark_part_as_main(
        robot_part_id="<YOUR-PART-ID>"
    )

    await cloud.mark_part_for_restart(
        robot_part_id="<YOUR-PART-ID>"
    )

    part_with_new_secret = await cloud.create_robot_part_secret(
        robot_part_id="<YOUR-PART-ID>"
    )

    part_with_new_secret = await cloud.get_robot_part(
    robot_part_id="<YOUR-PART-ID>"
    )
    print(part_with_new_secret.secrets[0])
    print(part_with_new_secret.secrets[1])
    print(part_with_new_secret.secret)

    await cloud.delete_robot_part_secret(
    robot_part_id="<YOUR-PART-ID>",
    secret_id="<YOUR-MACHINE-SECRET-ID-TO-DELETE>")

    part_with_new_secret = await cloud.get_robot_part(
    robot_part_id="<YOUR-PART-ID>"
    )
    print(part_with_new_secret.secrets[0])
    print(part_with_new_secret.secrets[1])
    print(part_with_new_secret.secret)

    list_of_machines = await cloud.list_robots(location_id="<YOUR-LOCATION-ID>")
    print(list_of_machines)

    new_machine_id = await cloud.new_robot(name="beepboop", location_id="<YOUR-LOCATION-ID>")
    print(f"New machine id: {new_machine_id}")

    updated_machine = await cloud.update_robot(
      robot_id="<YOUR-MACHINE-ID-TO-UPDATE-AND-DELETE>",
      name="Orange-Robot",
      location_id="<YOUR-LOCATION-ID>"
    )
    print(f"Updated machine: {updated_machine}")

    await cloud.delete_robot(robot_id="<YOUR-MACHINE-ID-TO-UPDATE-AND-DELETE>")

    fragments_list = await cloud.list_fragments(org_id="<YOUR-ORG-ID>", visibilities=[])
    print(fragments_list)

    the_fragment = await cloud.get_fragment(
      fragment_id="<YOUR-FRAGMENT-ID>")
    print("Name: ", the_fragment.name, "\nCreated on: ", the_fragment.created_on)

    new_fragment = await cloud.create_fragment(org_id="<YOUR-ORG-ID>", name="cool_smart_machine_to_configure_several_of")
    print(new_fragment)

    updated_fragment = await cloud.update_fragment(
    fragment_id="<YOUR-FRAGMENT-ID-TO-UPDATE-AND-DELETE>",
    name="better_name")
    print(f"Updated fragement: {updated_fragment}")

    await cloud.delete_fragment(
    fragment_id="<YOUR-FRAGMENT-ID-TO-UPDATE-AND-DELETE>")

    fragment_history = await cloud.get_fragment_history(
        id = "<YOUR-FRAGMENT-ID>",
        page_limit = 10
    )
    print(fragment_history)

    member_list, invite_list = await cloud.list_organization_members(org_id="<YOUR-ORG-ID>")
    second_user_id = member_list[0].user_id

    await cloud.add_role(
      org_id="<YOUR-ORG-ID>",
      identity_id=second_user_id,
      role="owner",
      resource_type="location",
      resource_id="<YOUR-LOCATION-ID>")
    
    await cloud.remove_role(
      org_id="<YOUR-ORG-ID>",
      identity_id=second_user_id,
      role="owner",
      resource_type="location",
      resource_id="<YOUR-LOCATION-ID>")
    
    await cloud.change_role(
      organization_id="<YOUR-ORG-ID>",
      old_identity_id=second_user_id,
      old_role="owner",
      old_resource_type="location",
      old_resource_id="<YOUR-LOCATION-ID>",
      new_identity_id=second_user_id,
      new_role="owner",
      new_resource_type="organization",
      new_resource_id="<YOUR-ORG-ID>")
    
    list_of_auths = await cloud.list_authorizations(
      org_id="<YOUR-ORG-ID>",
      resource_ids=["<YOUR-ORG-ID>"])
    print(list_of_auths)

    permissions = [AuthorizedPermissions(resource_type="organization",
                                     resource_id="<YOUR-ORG-ID>",
                                     permissions=["control_robot",
                                                  "read_robot_logs"])]

    filtered_permissions = await cloud.check_permissions(permissions)
    print(filtered_permissions)

    registry_items = await cloud.list_registry_items(
        organization_id="<YOUR-ORG-ID>",
        types=[PackageType.PACKAGE_TYPE_ML_TRAINING],
        visibilities=[Visibility.VISIBILITY_PRIVATE],
        platforms=[""],
        statuses=[RegistryItemStatus.REGISTRY_ITEM_STATUS_PUBLISHED]
    )

    item = await cloud.get_registry_item("viam:classification-tflite")
    print(item)

    registry_items = await cloud.list_registry_items(
        organization_id="",
        types=[PackageType.PACKAGE_TYPE_MODULE],
        visibilities=[Visibility.VISIBILITY_PUBLIC],
        platforms=["linux"],
        statuses=[RegistryItemStatus.REGISTRY_ITEM_STATUS_PUBLISHED]
    )

    print(registry_items)

    await cloud.create_registry_item("<YOUR-ORG-ID>", "test-create", PackageType.PACKAGE_TYPE_ML_MODEL)

    await cloud.update_registry_item("sierra:test-create", PackageType.PACKAGE_TYPE_ML_MODEL, "description", Visibility.VISIBILITY_PUBLIC)

    await cloud.delete_registry_item("sierra:test-create")

    new_module = await cloud.create_module(org_id="<YOUR-ORG-ID>", name="cool_new_hoverboard_module")
    print("Module ID:", new_module[0])

    model = Model(
        api="rdk:service:slam", 
        model="sierra:cool_new_hoverboard_module:wheeled"
    )

    url_of_my_module = await cloud.update_module(
      module_id="sierra:cool_new_hoverboard_module",
      url="https://docsformymodule.viam.com",
      models=[model],
      description="A base to support hoverboards.",
      entrypoint="exec")
    print(f"Module URL: {url_of_my_module}")

    registry_items = await cloud.list_registry_items(
        organization_id="",
        types=[PackageType.PACKAGE_TYPE_MODULE],
        visibilities=[Visibility.VISIBILITY_PUBLIC],
        platforms=["linux/any"],
        statuses=[RegistryItemStatus.REGISTRY_ITEM_STATUS_PUBLISHED]
    )
    print(registry_items)

    module_file_info = ModuleFileInfo(
        module_id = "sierra:cool_new_hoverboard_module",
        version = "1.0.0",
        platform = "darwin/arm64"
    )
  
    file_id = await cloud.upload_module_file(module_file_info=module_file_info, file=b"strain.png")
    print(file_id)

    the_module = await cloud.get_module(module_id="e76d1b3b-0468-4efd-bb7f-fb1d2b352fcb:aws-sagemaker")
    print(the_module)

    modules_list = await cloud.list_modules("<YOUR-ORG-ID>")
    print(modules_list)

    auth = APIKeyAuthorization(
      role='owner',
      resource_type="robot",
      resource_id="<YOUR-MACHINE-ID>"
    )

    print(auth)
    api_key, api_key_id = await cloud.create_key(org_id="<YOUR-ORG-ID>", 
                                                 authorizations=[auth],
                                                  name= "my_key")
    print(api_key)
    print(api_key_id)

    id, key = await cloud.rotate_key("<API-KEY-ID-TO-ROTATE>")
    print(id)
    print(key)

    keys = await cloud.list_keys("<YOUR-ORG-ID>")
    print(keys)

    api_key, api_key_id = await cloud.create_key_from_existing_key_authorizations(
    id="<API-KEY-ID-TO-DUPLICATE-AUTHORIZATIONS-FROM>")
    print(api_key)
    print(api_key_id)

    viam_client.close()

if __name__ == '__main__':
    asyncio.run(main())
