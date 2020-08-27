"""
purpose:
    Get rid of all nonascii characters given a string

author: emilyfan
last edited: 8/27
last edited: 7/1
"""
from confusables import normalize


def asciify(text: str, return_failed_chars=False):
    retstr = ""

    numconvchar = 0
    failedchars = []

    for char in text:
        if not char.isascii():
            newchar = normalize(char, prioritize_alpha=True)[0]

            # attempts to make newchar ascii
            if not newchar.isascii():
                if newchar == '—':
                    newchar = '--'
                    # print("YAY: " + char + " -> "+ newchar)
                else:
                    for posschar in normalize(char):
                        # print(char)
                        if posschar.isascii():
                            newchar = posschar
                            # print("YAY: " + char + " -> "+ newchar)
                            break

            if not newchar.isascii():
                # print("RIP this char cannot be processed: " + char + " -> "+ newchar)

                # print(char.encode('raw_unicode_escape'))
                # print(newchar.encode('raw_unicode_escape'))

                newchar = " "

                failedchars.append(char)

            else:
                numconvchar += 1
            # elif newchar not in ["'", '"', "...", '-']:
            # print("YAY: " + char + " -> "+ newchar)
            retstr += newchar
        else:
            retstr += char

    # print(str(numconvchar) + ' characters conversted to ASCII | ' + str(numfailedchar) + " failed")

    if return_failed_chars:
        return retstr, failedchars
    return retstr
