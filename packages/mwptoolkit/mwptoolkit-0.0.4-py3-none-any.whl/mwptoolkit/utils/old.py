import re
import json
import random
from copy import deepcopy
from collections import OrderedDict

import nltk
import stanza
from word2number import w2n

from mwptoolkit.utils.utils import read_json_data, str2float, lists2dict
from mwptoolkit.utils.enum_type import MaskSymbol, NumMask, SpecialTokens, EPT
from mwptoolkit.utils.data_structure import DependencyTree

def seg_and_tag_math23k(st, nums_fraction, nums):  # seg the equation and tag the num
    res = []
    pos_st = re.search(r"([+]|-|[*]|/|[(]|=)-(([(]\d+\.\d+[)])|([(]\d+/\d+[)]))", st)  #search negative number but filtate minus symbol
    if pos_st:
        p_start = pos_st.start() + 1
        p_end = pos_st.end()
        if p_start > 0:
            res += seg_and_tag_math23k(st[:p_start], nums_fraction, nums)
        try:
            st_num = str(eval(st[p_start:p_end]))
        except:  # % in number
            st_num = st[p_start:p_end]
        try:
            res.append(nums[st_num])
        except:
            try:
                number = str(int(eval(st_num)))
                if abs(eval(number) - eval(st_num)) < 1e-4:
                    res.append(nums[number])
                else:
                    res.append(st_num)
            except:
                res.append(st_num)
        if p_end < len(st):
            res += seg_and_tag_math23k(st[p_end:], nums_fraction, nums)
        return res
    for n in nums_fraction:
        if n in st:
            p_start = st.find(n)
            p_end = p_start + len(n)
            if p_start > 0:
                res += seg_and_tag_math23k(st[:p_start], nums_fraction, nums)
            try:
                res.append(nums[n])
            except:
                res.append(n)
            if p_end < len(st):
                res += seg_and_tag_math23k(st[p_end:], nums_fraction, nums)
            return res

    pos_st = re.search("\d+\.\d+%?|\d+%?", st)
    if pos_st:
        p_start = pos_st.start()
        p_end = pos_st.end()
        if p_start > 0:
            res += seg_and_tag_math23k(st[:p_start], nums_fraction, nums)
        st_num = st[p_start:p_end]
        try:
            res.append(nums[st_num])
        except:
            try:
                number = str(int(eval(st_num)))
                res.append(nums[number])
            except:
                res.append(st_num)
        if p_end < len(st):
            res += seg_and_tag_math23k(st[p_end:], nums_fraction, nums)
        return res
    for ss in st:
        res.append(ss)
    return res


def number_transfer_math23k(data, mask_type="number", min_generate_keep=0):
    r'''transfer num process

    Args:
        data: list.
        mask_type: str | default 'NUM', the way to mask num, optinal['NUM', 'alphabet', 'number'].
        min_generate_keep: int | default 5, the number to control if the numbers of equations will be kept as generating number.

    Return:
        processed_datas: list type.
        generate_number: list type, symbols to generate extra.
        copy_nums: int, the count of copied symbol from question to equation.
    '''
    if mask_type == MaskSymbol.NUM:
        sent_mask_list = NumMask.NUM
        equ_mask_list = NumMask.number
    elif mask_type == MaskSymbol.alphabet:
        sent_mask_list = NumMask.alphabet
        equ_mask_list = NumMask.alphabet
    elif mask_type == MaskSymbol.number:
        sent_mask_list = NumMask.number
        equ_mask_list = NumMask.number

    pattern = re.compile("\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?")

    generate_nums = []
    generate_nums_dict = {}
    copy_nums = 0
    processed_datas = []
    for d in data:
        #nums = []
        nums = OrderedDict()
        num_list = []
        input_seq = []
        seg = d["segmented_text"].split(" ")
        equations = d["equation"][2:]
        if '千' in equations:
            equations = equations[:equations.index('千')]
        num_pos_dict = {}
        # match and split number
        input_seq = []
        for s in seg:
            pos = re.search(pattern, s)
            if pos and pos.start() == 0:
                input_seq.append(s[pos.start():pos.end()])
                if pos.end() < len(s):
                    input_seq.append(s[pos.end():])
            else:
                if s == '　' or s == '':
                    continue
                input_seq.append(s)
        # find all num position
        for word_pos, word in enumerate(input_seq):
            pos = re.search(pattern, word)
            if pos and pos.start() == 0:
                if word in num_pos_dict:
                    num_pos_dict[word].append(word_pos)
                else:
                    num_list.append(word)
                    num_pos_dict[word] = [word_pos]
        num_list = sorted(num_list, key=lambda x: max(num_pos_dict[x]), reverse=False)
        nums = lists2dict(num_list, equ_mask_list[:len(num_list)])
        nums_for_ques = lists2dict(num_list, sent_mask_list[:len(num_list)])

        all_pos = []
        # number transform
        for num, mask in nums_for_ques.items():
            for pos in num_pos_dict[num]:
                input_seq[pos] = mask
                all_pos.append(pos)

        #input_seq = deepcopy(seg)
        nums_count = len(list(nums.keys()))
        if copy_nums < nums_count:
            copy_nums = nums_count

        nums_fraction = []
        for num, mask in nums.items():
            if re.search("\d*\(\d+/\d+\)\d*", num):
                nums_fraction.append(num)
        nums_fraction = sorted(nums_fraction, key=lambda x: len(x), reverse=True)

        out_seq = seg_and_tag_math23k(equations, nums_fraction, nums)
        for idx, s in enumerate(out_seq):
            # tag the num which is generated
            if s[0].isdigit() and s not in generate_nums and s not in num_list:
                generate_nums.append(s)
                generate_nums_dict[s] = 0
            if s in generate_nums and s not in num_list:
                generate_nums_dict[s] = generate_nums_dict[s] + 1

            if mask_type == MaskSymbol.NUM:
                if 'NUM' in s:
                    number = num_list[int(s[4:])]
                    if len(num_pos_dict[number]) > 1:
                        out_seq[idx] = number

        source = deepcopy(input_seq)
        for pos in all_pos:
            for key, value in num_pos_dict.items():
                if pos in value:
                    num_str = key
                    break
            num = str(str2float(num_str))
            source[pos] = num
        source = ' '.join(source)
        #get final number position
        num_pos = []
        for num in num_list:
            # select the latest position as the number position
            # if the number corresponds multiple positions
            num_pos.append(max(num_pos_dict[num]))
        assert len(num_list) == len(num_pos)
        #copy data
        # if d["id"]=="8883":
        #     print(1)
        new_data = d
        new_data["question"] = input_seq
        new_data["ques source 1"] = source
        new_data["equation"] = out_seq
        new_data["number list"] = num_list
        new_data["number position"] = num_pos
        processed_datas.append(new_data)

    generate_number = []
    for g in generate_nums:
        if generate_nums_dict[g] >= min_generate_keep:
            generate_number.append(g)
    return processed_datas, generate_number, copy_nums
