Feature: CryptoTransportLayer 

  Scenario: Connection
    Given there are 2 layers
    When layer 0 connects to layer 1
    Then layer 0 knows layer 1

    # fails
    Given there are 3 layers
    When layer 0 connects to layer 1
    and layer 1 connects to layer 2
    Then layer 0 knows layer 1
    and layer 1 knows layer 2
