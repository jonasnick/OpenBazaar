Feature: CryptoTransportLayer 

  Scenario: Connection
    Given there are 2 layers
    When layer 0 connects to layer 1
    Then layer 0 is aware of layer 1

    Given there are 3 layers
    When layer 0 connects to layer 1
    and layer 1 connects to layer 2
    Then layer 0 knows layer 1
    and layer 1 is aware of layer 2

  # Scenario: DHT
  #   Given there are 2 connected layers
  #   When layer 0 is added to routingtable of layer 1 
  #   and layer 1 is added to routingtable of layer 2
  #   Then findNode layer 1 in layer 0 succeeds
  #   and findNode layer 0 in layer 1 succeeds

