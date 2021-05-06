class VALUES:
    class EMPTY:
        num = 0
        desc = 'smth'
    class OTHER:
        num = 1
        desc = 'another'

    def __iter__(self):
        pass

x = 1
for cl in VALUES:
    print(cl)
