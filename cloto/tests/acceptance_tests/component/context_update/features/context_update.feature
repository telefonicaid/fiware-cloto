Feature: Update server context
  As a scalability manager user
  I want receive data from Monitoring
  In order to manage automatically the servers

  @basic
  Scenario Outline: Receive context with all parameters
    Given a "<server_id>" with one rule subscribed
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then the context is updated

    Examples:

      | server_id | cpu   | memory  | disk  | network |
      | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.00  | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.0     | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.8     | 0.0   | 0.15    |
      | qatest    | 0     | 0.8     | 0.1   | 0.0     |
      | qatest    | 0.75  | 0       | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.8     | 0     | 0.15    |
      | qatest    | 0.75  | 0.8     | 0.1   | 0       |
      | qatest    | 0.752 | 0.8     | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.857   | 0.1   | 0.15    |
      | qatest    | 0.75  | 0.8     | 0.123 | 0.15    |
      | qatest    | 0.75  | 0.8     | 0.1   | 0.151   |
      | qatest    | 0.75  | 0.8     | 0.1   | 1       |
      | qatest    | 0.75  | 0.8     | 1     | 0.151   |
      | qatest    | 0.75  | 1       | 0.1   | 0.151   |
      | qatest    | 1     | 0.8     | 0.1   | 0.151   |

  Scenario Outline: : Receive context with some parameters
    Given a "<server_id>" with one rule subscribed
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

      | server_id | cpu   | memory  | disk  | network | Error_code  | FaultElement  |
      | qatest    | None  | 0.8     | 0.1   | 0.15    | 400         | badRequest    |
      | qatest    | 0.00  | None    | 0.1   | 0.15    | 400         | badRequest    |
      | qatest    | 0.75  | 0.0     | None  | 0.15    | 400         | badRequest    |
      | qatest    | 0.75  | 0.8     | 0.0   | None    | 400         | badRequest    |
      | qatest    | None  | None    | None  | None    | 400         | badRequest    |
      | qatest    | None  | 0       | None  | 0.15    | 400         | badRequest    |


  Scenario Outline: : Receive context to not existent subscription_id
    Given a "<server_id>" with one rule subscribed
    And another "<subscription_id>" that not exist
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

      | subscription_id | server_id | cpu   | memory  | disk  | network | Error_code  | FaultElement  |
      | subscription1   | qatest    | None  | 0.8     | 0.1   | 0.15    | 400         | badRequest    |

  Scenario Outline: : Receive context to not existent server_id
    Given a "<server_id>" with one rule subscribed
    When context update is received to "<another_server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

      | another_server_id   | server_id | cpu   | memory  | disk  | network | Error_code  | FaultElement  |
      | existant_server     | qatest    | None  | 0.8     | 0.1   | 0.15    | 400         | badRequest    |
      | not_existant_server | qatest    | None  | 0.8     | 0.1   | 0.15    | 400         | badRequest    |

  Scenario Outline: : Receive context with incorrect attributes values

    Given a "<server_id>" with one rule subscribed
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id | cpu   | memory  | disk  | network | Error_code  | FaultElement  |
    | qatest    | 1.05  | 0.8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 5.8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 10.1  | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0.1   | 415.15  | 400         | badRequest    |
    | qatest    | -0.05 | 0.8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | -0.8    | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | -0.1  | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0.1   | -0.15   | 400         | badRequest    |
    | qatest    | 0,05  | 0.8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0,8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0,1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0.1   | 0,15    | 400         | badRequest    |
    | qatest    | hola  | 0.8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | tel     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | qas   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0.1   | test    | 400         | badRequest    |
    | qatest    | 0. 05 | 0.8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0. 8    | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0. 1  | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0.1   | 0. 15   | 400         | badRequest    |
    | qatest    | 0'05  | 0.8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0'8     | 0.1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0'1   | 0.15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0.1   | 0'15    | 400         | badRequest    |
    | qatest    |       | 0.8     | 0.1   | 0'15    | 400         | badRequest    |
    | qatest    | 0.05  |         | 0.1   | 0'15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     |       | 0'15    | 400         | badRequest    |
    | qatest    | 0.05  | 0.8     | 0.1   |         | 400         | badRequest    |



  Scenario Outline: Receive context with some constant parameter incorrect

    Given a "<server_id>" with one rule subscribed
    When context updated is receiver to "<server_id>" with constant "<constant_id>" incorrect
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id | constant_id |
    | qatest    | isPattern   |
    | qatest    | server_type |
    | qatest    | name        |
    | qatest    | at_type     |

  Scenario Outline: Receive context with some constant parameter missing

    Given a "<server_id>" with one rule subscribed
    When context updated is receiver to "<server_id>" with missing constant "<constant_id>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"

    Examples:

    | server_id | constant_id |
    | qatest    | isPattern   |
    | qatest    | server_type |
    | qatest    | name        |
    | qatest    | at_type     |


  @security
  Scenario Outline: : Receive context with incorrect token

    Given a "<server_id>" with one rule subscribed
    And incorrect "<token>"
    When context update is received to "<server_id>" with values "<cpu>", "<memory>", "<disk>" and "<network>"
    Then I obtain an "<Error_code>" and the "<FaultElement>"


    Examples:

    | server_id | cpu   | memory  | disk  | network | token     | Error_code  | FaultElement  |
    | qatest    | 0.75  | 0.8     | 0.1   | 0.15    | 1a2b3c    | 401         | unauthorized  |
    | qatest    | 0.75  | 0.8     | 0.1   | 0.15    | old_token | 401         | unauthorized  |
    | qatest    | 0.75  | 0.8     | 0.1   | 0.15    |           | 401         | unauthorized  |
    | qatest    | 0.75  | 0.8     | 0.1   | 0.15    | null      | 401         | unauthorized  |


