#The Iterator Pattern

The Iterator pattern has been implemented the python way:
[https://de.slideshare.net/DamianGordon1/python-the-iterator-pattern]

The Iterator itself is contained in the Iterator package in the DockerEnvironment.pythonBuild folder.
A unit test has been implemented in the Unittest folder next to the Iterator folder and
shows that the Iterator is actually working.

The iterator has been integrated in the connectToBot function, instead of creating and adding each
handler separate now a list of handlers is created and the iterator used to add them all to the dispatcher.
