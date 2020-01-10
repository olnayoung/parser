from initialize import tokenize
from parsing import Parser
from extra_funcs import from_list_to_str


### main function
def calcul(eq):

    # var_list = []
    # temp = input()
    # temp = temp.split(',')

    try:
        # if temp[0] != '':
        #     for n in range(len(temp)):
        #         var = temp[n].split(' ')
        #         if var[-1] == 'e':
        #             raise Exception("'e' is not available")
        #         var_list.append(var[-1])

        # eq = input()
        print('f =', eq)
        eq_list = tokenize(eq)
        print('tokens:', eq_list)

        E = Parser(eq_list)
        print('tree: ', str(E))
        ans = E.eval()
        # print('ans:', ans.a, ans.b, ans.c)

        return E.eval()

    except Exception as e:
        print('Error: ', e)
        return 'Error'


# if __name__ == "__main__":
# 	main()