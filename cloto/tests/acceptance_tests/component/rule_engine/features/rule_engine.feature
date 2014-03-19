Feature: As Scalability Manager
  I want fire some rules depending the facts arrived
  In order to offer scalability options


  Scenario Outline: Action fired when fact arrives and rule is satisfied
    Examples:
    | action_type |
    | scale_up    |
    | scale_down  |
    | notify      |

  Scenario Outline: Actions behaviour with only one attribute in conditions
    Examples:
    | action_fire | attribute |
    | YES         | CPU       |
    | YES         | memory    |
    | YES         | HD        |
    | YES         | Network   |
    | NO          | CPU       |
    | NO          | memory    |
    | NO          | HD        |
    | NO          | Network   |


  Scenario Outline: Actions behaviour with several attributes in conditions including operants
    Examples:

    | attributes                            |
    | CPU & memory                          |
    | CPU & network & HD                    |
    | CPU & network & HD & memory           |
    | CPU OR memory                         |
    | CPU OR network OR HD                  |
    | CPU OR network OR HD OR memory        |
    | (CPU OR network) AND (HD OR memory)   |
    | (CPU AND network) OR (HD AND memory)  |
