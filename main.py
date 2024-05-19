import glob
import os
import random
import time
import re
import collections
import threading

import keyboard  # pip install keyboard
import vlc # pip install python-vlc

player = vlc.MediaPlayer()

time_limit = 6

def main():
    global time_limit
    
    print("イントロクイズ！")
    print("正解だと思う曲の番号を四択から選んでね！")
    print(f"曲が流れる時間は{time_limit}秒だよ！\n")

    music_count = 1
    score = 0
    time_limit = 6
    total_time = 0
    stop = False

    genres = [os.path.basename(p.rstrip(os.sep)) for p in glob.glob(os.path.join('MusicData\\*'), recursive=True)]
    genres.insert(0, "全範囲")

    # ジャンル選択
    while True:
        print("ジャンルを以下から選択してね")

        for index, g in enumerate(genres, start=1):
            print(f"{index}: {g}", end="  ")

        print()
        
        genre = input(">>")

        if genre.isdigit():
            genre = int(genre)
            
            if 1 <= genre <= len(genres):
                if genre == 1:
                    musics_temp = [p for p in glob.glob(f"MusicData\\**", recursive=True) if os.path.isfile(p)]

                    if len(musics_temp) == 0:
                        os.system('cls')
                        print("楽曲が存在しません。他のジャンルを選択してください。\n")

                    else:
                        break
                else:
                    musics_temp = [p for p in glob.glob(f"MusicData\\{genres[genre - 1]}\\**", recursive=True) if os.path.isfile(p)]

                    if len(musics_temp) == 0:
                        os.system('cls')
                        print("楽曲が存在しません。他のジャンルを選択してください。\n")

                    else:
                        break
                
            else:
                os.system('cls')
                print(f"1~{len(genres)}の範囲で入力してください！\n")

        else:
            os.system('cls')
            print(f"数字の1~{len(genres)}の範囲で入力してください！\n")

    musics = []

    # 楽曲ファイル以外を除去して本リスト生成
    for i in range(len(musics_temp)):
        filename = musics_temp[i]

        if ("AlbumArtSmall" in filename) or ("Folder" in filename) or ("AlbumArt_{" in filename):
            #print(filename)
            pass

        else:
            musics.append(filename)
            
    music_names = [re.sub('^[0-9][0-9]-*','',os.path.splitext(os.path.basename(i))[0]) for i in musics]

    # 重複する楽曲の除去
    duplicated = [k for k, v in collections.Counter(music_names).items() if v > 1]

    for i in range(len(duplicated)):
        del musics[music_names.index(duplicated[i])]
        del music_names[music_names.index(duplicated[i])]

    os.system('cls')
    print(f"{genres[genre - 1]}ジャンル 出題範囲（全{len(musics)}曲）")
    
    print(music_names)
    print()

    while True:
        print(f"遊びたい曲数をきめてね (1~{len(musics)})")
        limit = input(">>")

        if limit.isdigit():
            limit = int(limit)

            if limit > len(musics) or limit <= 0:
                os.system('cls')
                print(f"曲数は1~{len(musics)}できめてね！\n")

            else:
                break

        else:
            os.system('cls')
            print(f"曲数は数字の1~{len(musics)}できめてね！\n")

    os.system('cls')
    print(f"{limit}問のイントロクイズを始めます。\nルールは簡単。曲名がわかったら【Enterキー】を押して、4択の中から曲名を選ぼう！曲が流れるのは最大6秒間だけだから、注意して聞こう！\n")
    print("> Enterキーを押してスタート < ")

    while True:
        event = keyboard.read_event()

        if event.name == 'enter':
            os.system('cls')
            break

    while stop == False:
        # 楽曲候補がなくなれば終了
        if music_count > limit:
            music_count -= 1
            break
        
        elif musics == []:
            break
        
        else:
            # 楽曲セレクト
            filename = random.choice(musics)
            musics.pop(musics.index(filename))
            
            music_name = re.sub('^[0-9][0-9]-*','',os.path.splitext(os.path.basename(filename))[0])
            player.set_mrl(filename)
            time.sleep(0.5) # これ抜いたらバグる
            player.play()
            print(f"{music_count}曲目、イントロドン！\n\n")
            print("> Enterキーで答える <\n")

            # 指定秒数 or キーが押下された
            start_time = time.time()
                
            while True:
                # 指定された秒数が経過したら処理を続行
                if time.time() - start_time >= time_limit:
                    print("時間切れ！\n")
                    tm = 6.00
                    time.sleep(0.7)
                    break

                # キーが押されたら処理を続行
                if keyboard.is_pressed("enter"):
                    input()
                    tm = round(time.time() - start_time, 2)
                    print("ぴんぽーん！")
                    time.sleep(0.7)
                    break
            
            player.stop()
            os.system('cls')

            # 回答の候補生成
            ans_list = [music_name]

            while len(ans_list) < 4:
                i = random.choice(music_names)
                
                if not i in ans_list:
                    ans_list.append(i)

            random.shuffle(ans_list)

            print(f"【{music_count}曲目】\n")
            print("さあ、曲の番号を入力してね！")
            print("-----")
            
            for i in range(4):
                print(f"{i + 1}. {ans_list[i]}")

            print("※わからないときは【0】")

            start_time = time.time()
            
            while True:
                answer = input(">>")

                if answer in ["1", "2", "3", "4", "0"]:
                    if ans_list[int(answer) - 1] == music_name:
                        os.system('cls')
                        #this_time = tm + (time.time() - start_time) # 回答を選ぶ時間もカウントするならこっち
                        this_time = tm
                        total_time += this_time
                        print(f"【{music_count}曲目】\n")
                        print(f"あなたの回答: {ans_list[int(answer) - 1]}\n")
                        print(f"正解！おめでとう！（タイム: {round(this_time, 2)}秒）")
                        time.sleep(0.5) # これ抜いたらバグる
                        score += 1
                        break
                    
                    elif answer == "0":
                        os.system('cls')
                        print(f"【{music_count}曲目】\n")
                        print("あなたの回答: なし")
                        print("ナイストライ！")
                        time.sleep(0.5) # これ抜いたらバグる
                        break

                    else:
                        os.system('cls')
                        print(f"【{music_count}曲目】\n")
                        print(f"あなたの回答: {ans_list[int(answer) - 1]}\n")
                        print("残念！不正解！")
                        time.sleep(0.5) # これ抜いたらバグる
                        break
                else:
                    os.system('cls')
                    print(f"【{music_count}曲目】\n")
                    print("半角1~4, 0で入力してね！\n")
                    print("さあ、曲の番号を入力してね！")
                    print("-----")
                    
                    for i in range(4):
                        print(f"{i + 1}. {ans_list[i]}")

                    print("※わからないときは【0】")
                
            print(f"答えは「{music_name}」でした！\n")
            print("> Enterキーを押して次へ / Escキーを押してこの曲で終了 <")

            while True:
                event = keyboard.read_event()

                if event.name == 'enter':
                    music_count += 1
                    os.system('cls')
                    break
                
                # Escが押された場合
                elif event.name == 'esc':
                    stop = True
                    os.system('cls')
                    break

    print("\nゲーム終了！")
    
    if score == music_count:
        print(f"{score}/{music_count}問正解！すばらしい！（正答率100% / タイム {round(total_time, 2)}秒）\n")

    else:
        print(f"{score}/{music_count}問正解！（正答率{int((score / music_count * 100))}%）\n")

    time.sleep(2)

    while True:
        print("もう一度プレイする？ (y/n)")
        yn = input(">>")

        if yn.lower() == "y":
            os.system('cls')
            main()
            break

        elif yn.lower() == "n":
            input("\n何かキーを押して終了します...")
            break

        else:
            os.system('cls')
            print("「y」か「n」でこたえてね\n")
            
main()
