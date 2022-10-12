import os 
FLAG='IngeHack{Y0U_F0und_M3}'

flag_bin = [format(ord(x), 'b') for x in FLAG]
subList = [flag_bin[n:n+4] for n in range(0, len(flag_bin), 4)]
print(subList)
print(flag_bin)
BASE_FOLDER = './New Folder/'
counter = 0
for  group in subList:
    if counter == 0:
        subfolder = 'New Folder '
        os.mkdir(BASE_FOLDER+subfolder)
    else:
        subfolder = f'New Folder ({counter})'
        os.mkdir(BASE_FOLDER+subfolder)
    
    for i, bytes in enumerate(group):
        if i ==0:
            subsubfolder = 'New Folder '
        else:
            subsubfolder = f'New Folder ({i})'
        os.mkdir(BASE_FOLDER+subfolder+'/'+subsubfolder)
        elem = '0'*(8-len(bytes))+ bytes
        print(elem)
        for j, bit in enumerate(elem):
            if j == 0:
                subsubsubfolder = 'New Folder '
            else:
                subsubsubfolder = f'New Folder ({j})'
            os.mkdir(BASE_FOLDER+subfolder+"/"+subsubfolder+'/'+subsubsubfolder+'/')
            if int(bit)==1:
                f = open(BASE_FOLDER+subfolder+ "/" + subsubfolder+'/'+subsubsubfolder+'/flag.txt','w')
                f.write('IngeHack{This_is_not_the_flag}')
                f.close()
    counter = counter +1 



