**Version 1:**

Tỉ lệ augment data:
+ 20%: 
    
    lỗi về dấu
    
        random_remove_accent: 0.3
        change_accent: 0.3
        remove_accent_sent: 0.4
    
+ 20%:
    
    augment_sent = 2 : 0.3
    
    lỗi với một từ : 0.15 
    
        change_first_char: 0.25
        change_type_telex: 0.2
        convert_typing_missing_char: 0.1
        convert_random_word_distance_keyboard: 0.15
        convert_last_char_distance_keyboard: 0.2
        convert_first_char_distance_keyboard: 0.1
        
+ 10% :

    gộp 2 lỗi dấu và từ:
        
        lỗi dấu vẫn như phần 1
        change_first_char: 0.15
        change_type_telex: 0.15
        convert_typing_missing_char: 0.15
        convert_random_word_distance_keyboard: 0.15
        convert_last_char_distance_keyboard: 0.3
        convert_first_char_distance_keyboard: 0.1
        
+ 20%:

    lỗi câu:
    
        remove_split_word: 0.3
        random_del_word: 0.1
        random_remove_accent + random_del_word: 0.1
        random_remove_accent + remove_split_word: 0.3
        add_char_in_last_word: 0.2
        

**Version 2:**

Tỉ lệ số câu lỗi sinh ra phụ thuộc vào chiều dài:

    if prob < 0.7:
        if len(text_src) > 25:
            n_augment_sent = random.choice([2, 3])
        elif 15 < len(split_word_with_bound(text_src)) <= 25:
            n_augment_sent = random.choice([1, 2])


+ 20%:

    lỗi một từ 15%:
        
        change_type_telex: 0.2
        convert_typing_missing_char: 0.2
        convert_random_word_distance_keyboard: 0.15
        convert_last_char_distance_keyboard: 0.2
        convert_first_char_distance_keyboard: 0.1
        add_char_in_last_word: 0.15
        
+ 15%:

    remove_split_word : 0.15 
    
    lỗi 1 từ : 0.1
    
        random_remove_accent:0.15
        change_type_telex: 0.05
        convert_typing_missing_char: 0.2
        convert_random_word_distance_keyboard: 0.15
        convert_last_char_distance_keyboard: 0.2
        convert_first_char_distance_keyboard: 0.05
        add_char_in_last_word: 0.2
    
     random_del_word: 0.3 
     
+ 15%: 
    
    lỗi 1 từ: 0.1
    
        random_remove_accent:0.15
        change_type_telex: 0.05
        convert_typing_missing_char: 0.2
        convert_random_word_distance_keyboard: 0.15
        convert_last_char_distance_keyboard: 0.2
        convert_first_char_distance_keyboard: 0.05
        add_char_in_last_word: 0.2
        
    change_accent: 0.3
    
    change_first_char: 0.3
    
+ 10%:

        0.2 :
            remove_split_word
            change_accent

        0.2 :
            change_first_char
            random_del_word

        0.2 :
            change_accent
            random_del_word

        0.15:
            remove_split_word
            change_first_char
             
+ 10%:

    remove_split_word : 0.2
    
    lỗi 1 từ : 0.1
    
        random_remove_accent:0.15
        change_type_telex: 0.05
        convert_typing_missing_char: 0.2
        convert_random_word_distance_keyboard: 0.15
        convert_last_char_distance_keyboard: 0.2
        convert_first_char_distance_keyboard: 0.05
        add_char_in_last_word: 0.2
    
     change_first_char: 0.3
     
     change_accent: 0.3
     
     random_del_word: 0.4
     


**Version 3**

Thêm các lỗi:

    Thêm từ bất kì vào câu
    Biến đổi từ và làm từ đó sai
    
 
     
    



        
        

    
        
        
        
        
      
     
