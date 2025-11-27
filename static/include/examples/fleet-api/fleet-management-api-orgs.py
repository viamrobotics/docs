import asyncio
import os
import time

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.proto.app import Authorization
from viam.proto.app import AuthorizedPermissions
from viam.proto.app.packages import PackageType
from viam.proto.app import Visibility, RegistryItemStatus
from viam.proto.app import Model, ModuleFileInfo
from viam.app.app_client import APIKeyAuthorization

# Configuration constants – replace with your actual values
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings
ORG_ID = ""  # Organization ID, find or create in your organization settings
EMAIL_ADDRESS = ""  # Email address of the user to get the user id for
LOCATION_ID = ""  # Location ID, find or create in your organization settings

# :remove-start:
ORG_ID = os.environ["TEST_ORG_ID"]
ORG_ID_2 = "b5e9f350-cbcf-4d2a-bbb1-a2e2fd6851e1"
API_KEY = os.environ["VIAM_API_KEY"]
API_KEY_ID = os.environ["VIAM_API_KEY_ID"]
LOCATION_ID = "pg5q3j3h95"
TEST_EMAIL = os.environ["TEST_EMAIL"]
# :remove-end:

async def connect() -> ViamClient:
    dial_options = DialOptions(
      credentials=Credentials(
        type="api-key",
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        payload=API_KEY,
      ),
      # Replace "<API-KEY-ID>" (including brackets) with your machine's
      # API key ID
      auth_entity=API_KEY_ID
    )
    return await ViamClient.create_from_dial_options(dial_options)

async def main():
    async with await connect() as viam_client:
        # Instantiate an AppClient called "cloud"
        # to run fleet management API methods on
        cloud = viam_client.app_client

        # TODO: internal only
        # id = await cloud.get_user_id_by_email(EMAIL_ADDRESS)
        # print(f"USER ID: {id}")

        # TODO: internal only
        # organization = await cloud.create_organization("example-org")
        # print(f"Organization: {organization}")

        org_list = await cloud.list_organizations()
        assert len(org_list) > 0
        assert org_list[0].id == ORG_ID

        org_list = await cloud.get_organizations_with_access_to_location(LOCATION_ID)
        assert len(org_list) > 0
        assert org_list[0].id == ORG_ID

        member_list, invite_list = await cloud.list_organization_members(org_id=ORG_ID)
        assert len(member_list) > 0


        # TODO: internal only
        # org_list = await cloud.list_organizations_by_user(first_user_id)
        # print(org_list)

        org = await cloud.get_organization(ORG_ID)
        assert org.id == ORG_ID

        org_namespace = "test-org-namespace-unavailable"
        available = await cloud.get_organization_namespace_availability(
            public_namespace=org_namespace
        )
        assert available

        organization = await cloud.update_organization(
          org_id=ORG_ID,
          name="docs-scheduled-tests"
        )
        assert organization.name == "docs-scheduled-tests"

        # CANT TEST
        # await cloud.delete_organization("298d2032-7a63-4a7f-810c-0a841e219bd9")

        await cloud.create_organization_invite(ORG_ID, TEST_EMAIL)
        _, invite_list = await cloud.list_organization_members(org_id=ORG_ID)
        assert len(invite_list) >= 1
        assert invite_list[0].email == TEST_EMAIL

        update_invite = await cloud.update_organization_invite_authorizations(
            org_id=ORG_ID,
            email=TEST_EMAIL,
            add_authorizations=[Authorization(
                authorization_type="role",
                authorization_id="location_owner",
                resource_type="location",
                resource_id=LOCATION_ID,
                organization_id=ORG_ID,
                identity_id="",
            )])
        assert update_invite.authorizations[1].authorization_id == "location_owner"

        org_invite = await cloud.resend_organization_invite(ORG_ID, TEST_EMAIL)
        assert org_invite.email == TEST_EMAIL

        await cloud.delete_organization_invite(ORG_ID, TEST_EMAIL)
        _, invite_list_now = await cloud.list_organization_members(org_id=ORG_ID)
        assert len(invite_list_now) == len(invite_list) - 1

        # CANT TEST
        # await cloud.delete_organization_member(org_id="<YOUR-ORG-ID>", user_id=first_user_id)

        new_location = await cloud.create_location(org_id=ORG_ID, name="Robotville", parent_location_id=LOCATION_ID)
        assert new_location.name == "Robotville"

        location = await cloud.get_location(location_id=new_location.id)
        assert location.name == "Robotville"

        updated_location = await cloud.update_location(
            location_id=new_location.id,
            name="Robotville 2",
            parent_location_id=LOCATION_ID,
        )
        assert updated_location.name == "Robotville 2"

        await cloud.share_location(organization_id=ORG_ID_2, location_id=new_location.id)
        await cloud.unshare_location(organization_id=ORG_ID_2, location_id=new_location.id)

        loc_auth = await cloud.location_auth(location_id=new_location.id)
        assert loc_auth.location_id == new_location.id

        new_loc_auth = await cloud.create_location_secret(location_id=new_location.id)
        assert new_loc_auth.location_id == new_location.id

        await cloud.delete_location_secret(
            location_id=new_loc_auth.location_id,
            secret_id=new_loc_auth.secrets[0].id)

        loc_auth = await cloud.location_auth(location_id=new_location.id)
        assert len(loc_auth.secrets) == 1

        await cloud.delete_location(location_id=new_location.id)
        locations = await cloud.list_locations(ORG_ID)
        assert len(locations) == 2

        keys = await cloud.list_keys(ORG_ID)
        num_keys = len(keys)

        api_key, api_key_id = await cloud.create_key(
            org_id=ORG_ID,
            authorizations=[APIKeyAuthorization(
                role='owner',
                resource_type="location",
                resource_id=LOCATION_ID
            )],
            name="mytestkey")
        assert api_key is not None
        assert api_key_id is not None


        new_api_key, new_api_key_id = await cloud.rotate_key(api_key_id)
        assert new_api_key_id is not None
        assert new_api_key is not None
        assert api_key != new_api_key
        keys = await cloud.list_keys(ORG_ID)
        new_num_keys = len(keys)
        assert new_num_keys == num_keys + 1

        api_key, api_key_id = await cloud.create_key_from_existing_key_authorizations(
            id=new_api_key_id)
        assert api_key is not None
        assert api_key_id is not None
        keys = await cloud.list_keys(ORG_ID)
        new_num_keys2 = len(keys)
        assert new_num_keys2 == num_keys + 2
        await cloud.delete_key(api_key_id)
        await cloud.delete_key(new_api_key_id)
        keys = await cloud.list_keys(ORG_ID)
        new_num_keys = len(keys)
        assert new_num_keys == num_keys

        # setup
        user_id = member_list[-1].user_id

        await cloud.add_role(
          org_id=ORG_ID,
          identity_id=user_id,
          role="owner",
          resource_type="location",
          resource_id=LOCATION_ID)

        member_list, _ = await cloud.list_organization_members(org_id=ORG_ID)

        list_of_auths = await cloud.list_authorizations(
          org_id=ORG_ID,
          resource_ids=[LOCATION_ID])
        current_auths_location = len(list_of_auths)
        assert current_auths_location >= 1

        await cloud.change_role(
          organization_id=ORG_ID,
          old_identity_id=user_id,
          old_role="owner",
          old_resource_type="location",
          old_resource_id=LOCATION_ID,
          new_identity_id=user_id,
          new_role="owner",
          new_resource_type="organization",
          new_resource_id=ORG_ID)

        list_of_auths = await cloud.list_authorizations(
          org_id=ORG_ID,
          resource_ids=[LOCATION_ID])
        assert len(list_of_auths) == 0

        list_of_auths = await cloud.list_authorizations(
          org_id=ORG_ID,
          resource_ids=[ORG_ID])
        current_auths_org = len(list_of_auths)
        assert current_auths_org >= 1

        await cloud.remove_role(
          org_id=ORG_ID,
          identity_id=user_id,
          role="owner",
          resource_type="organization",
          resource_id=ORG_ID)

        list_of_auths = await cloud.list_authorizations(
          org_id=ORG_ID,
          resource_ids=[ORG_ID])
        assert len(list_of_auths) == current_auths_org - 1


        permissions = [AuthorizedPermissions(resource_type="organization",
                                        resource_id=ORG_ID,
                                        permissions=["control_robot",
                                                      "read_robot_logs"])]

        filtered_permissions = await cloud.check_permissions(permissions)
        assert len(filtered_permissions) == 1
        assert filtered_permissions[0].resource_type == "organization"
        assert filtered_permissions[0].resource_id == ORG_ID


if __name__ == '__main__':
    asyncio.run(main())
