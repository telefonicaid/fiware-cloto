Feature: Policy Manager information
    In order to check the information
    operations related to Policy Manager,
    We'll implement several integration
    test to check that it is working
    properly.

    @basic
    Scenario: Get tenant information in the Policy Manager
      Given a created tenant
      When I retrieve the tenant information
      Then I get the following information:
      | doc                                          | owner          | version | windowsize |
      | https://forge.fi-ware.org/plugins/mediawiki/wiki/fiware/index.php/Policy_Manager_Open_RESTful_API_Specification | Telefonica I+D | 1.5.0     | 5          |


    Scenario Outline: Get not existant tenant information
      Given the tenant "<tenant_id>"
      When I retrieve the tenant information
      Then I obtain an "<Error_code>" and the "<FaultElement>"

      Examples:

      | tenant_id | Error_code| FaultElement  |
      | toni      | 401       | unauthorized  |

    @security
    Scenario Outline: Get tenant information with incorrect token authentication

      Given a created tenant
      And incorrect "<token>"
      When I retrieve the tenant information
      Then I obtain an "<Error_code>" and the "<FaultElement>"

      Examples:

      | Error_code  | FaultElement  | token     |
      | 401         | unauthorized  | 1a2b3c    |
      | 401         | unauthorized  | old_token |
      | 401         | unauthorized  |           |
      | 401         | unauthorized  | null      |
