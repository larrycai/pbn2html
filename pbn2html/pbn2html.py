#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import sys
import pkgutil
if "pbn2html" in os.environ.get("_"):
    from .pbn_parser import importPBN
else:
    from pbn_parser import importPBN
from string import Template

language="Chinese"

html_template="""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="Generator" content="pbn2html toolkit">
    <title>Enjoy the bridge game</title>
  </head>
  <body class=bcbody>
    <!-- Credit to BridgeComposer Version 5.83 (64 bit) - https://bridgecomposer.com/ -->
    <div class=bcboard style="text-align: center">
        $all
  </body>
</html>
"""
card_template="""
              <table class=bchand style="border-collapse: collapse; border-spacing: 0">
                <tr class=bchand>
                  <td class=bcpip style="font: 10pt Verdana, sans-serif; padding: 1px; padding-top: 0; padding-bottom: 0; width: 1em; text-align: center"><span class=bcspades>&spades;</span></td>
                  <td class=bchand style="font: 10pt Verdana, sans-serif; padding: 1px; padding-top: 0; padding-bottom: 0">$spade</td>
                </tr>
                <tr class=bchand>
                  <td class=bcpip style="font: 10pt Verdana, sans-serif; padding: 1px; padding-top: 0; padding-bottom: 0; width: 1em; text-align: center"><span class=bchearts style="color: red">&hearts;</span></td>
                  <td class=bchand style="font: 10pt Verdana, sans-serif; padding: 1px; padding-top: 0; padding-bottom: 0">$heart</td>
                </tr>
                <tr class=bchand>
                  <td class=bcpip style="font: 10pt Verdana, sans-serif; padding: 1px; padding-top: 0; padding-bottom: 0; width: 1em; text-align: center"><span class=bcdiams style="color: red">&diams;</span></td>
                  <td class=bchand style="font: 10pt Verdana, sans-serif; padding: 1px; padding-top: 0; padding-bottom: 0">$diamond</td>
                </tr>
                <tr class=bchand>
                  <td class=bcpip style="font: 10pt Verdana, sans-serif; padding: 1px; padding-top: 0; padding-bottom: 0; width: 1em; text-align: center"><span class=bcclubs>&clubs;</span></td>
                  <td class=bchand style="font: 10pt Verdana, sans-serif; padding: 1px; padding-top: 0; padding-bottom: 0">$club</td>
                </tr>
              </table>
            </td>
"""

board_template="""
              <table class=bcct style="width: 4em; height: 4em; border-collapse: collapse; font: 10pt @微软雅黑, sans-serif; color: #ffffff; border: 1px solid #aaaaaa">
                <tr class=bcct1>
                  <td class=bcct1 style="text-align: center; vertical-align: text-top; padding: 1px"></td>
                  <td class=bcct1 style="text-align: center; vertical-align: text-top; padding: 1px;background-color: $ns_vulnerable;">北</td>
                  <td class=bcct1 style="text-align: center; vertical-align: text-top; padding: 1px"></td>
                </tr>
                <tr class=bcct2>
                  <td class=bcct2a style="text-align: left; vertical-align: text-top; padding: 1px; background-color: $ew_vulnerable;">西</td>
                  <td class=bcct2b style="text-align: center; padding: 1px; color: black;">$dealer</td>
                  <td class=bcct2c style="text-align: right; vertical-align: text-top; padding: 1px; background-color: $ew_vulnerable;">东</td>
                </tr>
                <tr class=bcct3>
                  <td class=bcct3 style="text-align: center; vertical-align: text-top; padding: 1px"></td>
                  <td class=bcct3 style="text-align: center; vertical-align: text-top; padding: 1px; background-color: $ns_vulnerable;">南</td>
                  <td class=bcct3 style="text-align: center; vertical-align: text-top; padding: 1px"></td>
                </tr>
              </table>
"""
extra_template="""
            <td class=bchd3 style="padding: 1px; font: 10pt Verdana, sans-serif; padding: 1px; text-align: left; vertical-align: top;">定约: $declarer $contract</td>
"""

auction_template="""
          $auction
"""

def html_card(cards):
    src = Template(card_template)
    all = {
        "spade" : cards["S"],
        "heart" : cards["H"],
        "diamond" : cards["D"],
        "club" : cards["C"]
    }
    return src.safe_substitute(all)

def html_board(vulnerable, dealer):
    arrows={"S": "&darr;","W": "&larr;","N": "&uarr;","E": "&rarr;"}
    src = Template(board_template)
    
    NONE_COLOR="green"
    VULNERABLE_COLOR="red"

    all = {}
    if vulnerable == "NS":
        all["ns_vulnerable"]= VULNERABLE_COLOR
        all["ew_vulnerable"]= NONE_COLOR
    elif vulnerable == "EW":
        all["ew_vulnerable"]= VULNERABLE_COLOR
        all["ns_vulnerable"]= NONE_COLOR
    elif vulnerable == "NONE":
        all["ew_vulnerable"]= NONE_COLOR
        all["ns_vulnerable"]= NONE_COLOR
    else:
        all["ew_vulnerable"]= VULNERABLE_COLOR
        all["ns_vulnerable"]= VULNERABLE_COLOR
    all["dealer"] = arrows[dealer]
    
    return src.safe_substitute(all)

def bid_css(contract):
    rank = contract[0]
    suit = contract[1:]
    css = rank
    space="<span style='font: 10pt Times, serif'>&thinsp;</span>"
    suit_css = {
        'S':  space + "<span class=bcspades style='font: 10pt Verdana, sans-serif;'>&spades;</span>",
        "H":  space + "<span class=bchearts style='color: red; font: 10pt Verdana, sans-serif;'>&hearts;</span>",
        "D":  space + "<span class=bcdiams style='color: red; font: 10pt Verdana, sans-serif;'>&diams;</span>",
        "C":  space + "<span class=bcclubs style='font: 10pt Verdana, sans-serif;'>&clubs;</span>",
        "NT": space + "NT",
    }
    if contract in [ "AP", "Pass", "X", "XX" ]:
        css = contract
    else:
        css += suit_css[suit]
    return css
    
def html_extra(contract, declarer):
    src = Template(extra_template)
    css = bid_css(contract)
    trans_declarer={"S": "南","W": "西","N": "北","E": "东"}

    all = { "declarer": trans_declarer[declarer], "contract" : css}
    return src.safe_substitute(all)

def html_auction(auction, section_auction):
    src = Template(auction_template)
    # need insert empty cell based on auction
    position="WNES" 
    empty_cells = position.index(auction)

    # handle ==1==, 6D?, 6D!
    filtered_auction = [x for x in section_auction.split() if not x.startswith("=")]
    # print(filtered_auction)
    css = "<tr class=bcauction>"
    col = 0
    for empty in range(empty_cells):
        css += "<td class=bcauction style='padding: 1px; text-align: left; white-space: nowrap'></td>\n"
        col += 1
    for one in filtered_auction:
        # print("aution:", one)
        one = one.replace("!", '').replace("?","")
        css +="<td class=bcauction style='padding: 1px; text-align: left; white-space: nowrap'>%s</td>\n" %  bid_css(one)
        if col == 3:
            col = 0
            css += "</tr>\n"
        else:
            col += 1
    css += "</tr>\n"
    all = { "auction": css}
    return src.safe_substitute(all)

def pbn2html(pbn_file):
    all = {
        "generated" : "2020-12-01"
    }
    
    # handle multiple pbn in one file
    pbnstr = open(pbn_file,encoding="utf-8" ).read()
    delimiter="[Event"
    pbns =  [delimiter+e for e in pbnstr.split(delimiter) if "Deal" in e]
    result = ""
    #print(pbns)
    for pbn in pbns:
        #print("hha", pbn)
        tags, hands, section_auction = importPBN(pbn)
    
        # print(tags, hands,section_auction)
        all["title"] = tags["Event"]
        all["north"] = html_card(hands["N"])
        all["west"] = html_card(hands["W"])
        all["east"] = html_card(hands["E"])
        all["south"] = html_card(hands["S"])
        all["board"] = html_board(tags["Vulnerable"],tags["Dealer"])
        all["extra"] = html_extra(tags["Contract"],tags["Declarer"])
        all["auction"] = html_auction(tags["Auction"], section_auction)
        # hacked solution to check whether it is module or local
        # > _: C:/Python36/Scripts/pbn2html
        if "pbn2html" in os.environ.get("_"):
            template = pkgutil.get_data(__name__,'template.html')
            src = Template(template.decode('utf-8'))
        else:
            template = open("template.html", "r",encoding="utf-8").read()
            src = Template(template)
        result += src.safe_substitute(all)
        #print(len(result))
    src = Template(html_template)
    all = { "all": result }
    result = src.safe_substitute(all)
    output = os.path.splitext(pbn_file)[0]+'.html'
    with io.open(output, "w", encoding="utf-8") as text_file:
        print("write to file %s" % output)
        text_file.write(result)


def main():
    # print(sys.argv)
    if len(sys.argv) > 1:
        param = sys.argv[1:]
        if param[0].endswith(".pbn"):
            pbn2html(param[0])
        else:
            print("pbn2html.py <file.pbn>")
    else:
        print("pbn2html.py <file.pbn>")

if __name__ == '__main__':
    main()
