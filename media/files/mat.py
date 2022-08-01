import random
cal = 0

kata_list = []
kata = 'ksn' * 2
while True:
    new = ''.join(random.sample(kata, 5))
    if new not in kata_list:
        kata_list.append(new)

    
    
    if kata_list:
        ind = kata_list[cal]
        ind = ind.index('k')
        if 'k' == kata_list[cal][ind]:
            break

    cal += 1

print(len(kata_list))