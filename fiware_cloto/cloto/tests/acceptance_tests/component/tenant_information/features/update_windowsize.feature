Feature: Policy Manager update window size
    In order to configure the data required to fire a rule
    As a user
    I want update the tenant window size

    @basic
    Scenario Outline: Update window size
        Given a created tenant
        When I update the "<windowsize>"
        Then the "<windowsize>" is update in Policy Manager

        Examples:

        |   windowsize  |
        |   1           |
        |   2           |
        |   10          |


    Scenario Outline: Incorrect update window size requests

        Given a created tenant
        When I update the "<windowsize>"
        Then I obtain an "<Error_code>" and the "<FaultElement>"

        Examples:

        |   windowsize  |   Error_code  |   FaultElement    |
        |   -1          |   400         |   badRequest      |
        |   0           |   400         |   badRequest      |
        |   zero        |   400         |   badRequest      |
        |   5.0         |   400         |   badRequest      |
        |   3,0         |   400         |   badRequest      |
        |   1'0         |   400         |   badRequest      |
        |   1E          |   400         |   badRequest      |
        |   11          |   400         |   badRequest      |
        |   '1'         |   400         |   badRequest      |


    Scenario: Update window size from not existent tenant information
        Given the tenant "<tenant_id>"
        When I update the "<windowsize>"
        Then I obtain an "<Error_code>" and the "<FaultElement>"

        Examples:

        |   tenant_id   |   Error_code  |    FaultElement    |  windowsize  |
        |   toni        |   401         |    unauthorized    |  3           |

    @security
    Scenario Outline: Update window size with incorrect token authentication

        Given a created tenant
        And incorrect "<token>"
        When I update the "<windowsize>"
        Then I obtain an "<Error_code>" and the "<FaultElement>"

        Examples:

        |   Error_code  |   FaultElement    |   token     | windowsize  |
        |   401         |   unauthorized    |   1a2b3c    | 3           |
        |   401         |   unauthorized    |   old_token | 3           |
        |   401         |   unauthorized    |             | 3           |
        |   401         |   unauthorized    |   null      | 3           |
