__author__ = 'Matteo'
__doc__="""What characters are allowed as variable names?"""
naughty={"Type":[],"Syntax":[],"UnicodeEncode":[],"Indentation":[]}
nice=[]
max
#8 bytes are 32bit
for i in range(0,2**999):
    try:
        name=chr(i)
    except:
        big=i
        break

print(big)
for i in range(0,big):
    state="unknown"
    try:
        exec(name + "='Hello World'")
        nice.append(name)
        state="nice"
    except (TypeError, SyntaxError,UnicodeEncodeError) as e:
        flavor=str(e.__class__).replace("<class '","").replace("Error'>","")
        naughty[flavor].append(name)
        state="naughty"
    finally:
        #print(name+" "+state)
        pass

print("Nice: "+", ".join(nice))

#There are dodgy characters in here that delete shit.
"""
for k in naughty.keys():
    if k == "UnicodeEncode":
        next
    else:
        print(str(k)+": "+", ".join(naughty[k]))
"""