import time   
import sys
import random
import pickle
def register():
    global idpw
    global idstat
    temp_id=input("사용하실 아이디를 입력해주세요.\n") #임시아이디(적합성판단용)
    if len(temp_id) <= 0:
        print("무엇도 입력하지 않을 순 없습니다.") #아무것도 입력하지 않을 시 생성불가.
        time.sleep(0.5)
        register()
    elif ' ' in temp_id:
        print("아이디에는 공백이 들어갈 수 없습니다.") #띄어쓰기시 생성불가.
        time.sleep(0.5)
        register()
    elif temp_id in idpw.keys():
        print("이미 존재하는 아이디 입니다.") #중복존재시 생성불가
        time.sleep(0.5)
        register()
    else:
        cho=input("ID: %s  확정하시려면 Y를 입력해주세요.\n"%(temp_id)) #임시아이디가 적합할때 정말사용할지 재확인
        if cho == 'Y' or cho=='y':
            while True:
                pw1=input("사용하실 비밀번호를 입력해주세요\n")  #비밀번호 설정
                pw2=input("동일한 비밀번호를 입력해주세요\n")  #비밀번호 재검증
                if pw1 == pw2:
                    idpw[temp_id]=pw1  #비밀번호가 같다면, idpw 딕셔너리에 id와password를 key값과 value값에 저장.
                    idstat[temp_id]={"nick":temp_id,"Lv":1,"exp":0,"achieve":{"찍신!(업다운 1번만에 클리어)":False,\
                        "타고난 승부사(벅샷룰렛에서 피해를 입지않고 클리어)":False, "빠른 클리어(야구게임에서 5번 시도 내 클리어)":False, \
                            "뭘해도(하이로우에서 하이, 로우, 미들 전부 승리)":False},"title":[],"now_title":''}
                    #기본정보 생성
                    #닉네임, 레벨, 경험치, 업적, 칭호 설정.
                    print("아이디 등록완료.")
                    return
                else:
                    print("비밀번호가 다릅니다.")
        else:
            time.sleep(0.5)
            register() #확정취소시 다시 회원가입절차로 재귀
            
            
def login():
    global idpw
    global idstat
    global now_login
    enter_id=input("아이디 : ") #아이디입력
    if enter_id == "regi":
        return register() #regi입력시 아이디생성으로 이동
    enter_pw=input("비밀번호 : ") #비밀번호입력
    if enter_id not in idpw: #idpw 딕셔너리에 id 존재검증

        print("존재하지 않는 아이디 입니다. 회원가입하시려면 regi를 입력해주세요.")
        time.sleep(0.4)
        login()
    else:
        if enter_pw == idpw[enter_id]: #해당 id의 비밀번호 검증
            now_login=enter_id #현재로그인에 정보 저장
            print("로그인완료. 환영합니다 %s 님."%(idstat[now_login]['nick']))
        else:
            print("비밀번호가 틀립니다.")
            time.sleep(0.4)
            login()
def remove_id():
    global now_login
    checkpw=input("비밀번호 입력 : ") #비밀번호 확인
    if checkpw == idpw[now_login]:
        while True:
            try: #int() 함수 시도 후 실패시 except로 (숫자검증)
                check=int(input("정말 삭제하시겠습니까?\n1.예\n2.아니오\n"))
                if check == 1:
                    del idstat[now_login] #id와 관련된 딕셔너리 삭제
                    del idpw[now_login]
                    now_login=''
                    print("아이디 삭제완료. 안녕히 가십시오.")
                    return
                elif check == 2:
                    print("취소.")
                    return
            except:
                print("숫자를 입력해주세요.") #숫자가 아닐경우 출력
            
def change_nick():
    global idpw
    global idstat
    global now_login

    checkpw=input("비밀번호 : ") #비밀번호 검증
    if checkpw == idpw[now_login]:
        temp_nick=input("현재 닉네임 : %s\n변경하실 닉네임 : "%(idstat[now_login]['nick']))
        idstat[now_login]["nick"]=temp_nick #idstat 딕셔너리의 nick 밸류값을 바꿈.
    else:
        print("비밀번호 오류")
        return

def logout():
    global now_login
    now_login='' #현재로그인 정보를 공백으로 비움.
    print("로그아웃")
    
def achmap(item): #업적을 예쁘게 출력하기 위한 함수
  if item[1] == True: #업적 딕셔너리를 아이템으로 불러와 value값이 True일때 O를 출력
      ox = "O"
  else:
      ox = "X"
  return item[0] + ": " + ox #키값과 if문에서 설정된 ox를 붙여서 반환

def allclear(): #설정된 업적을 모두 달성했는지 검증
    if 'allclear' not in idstat[now_login]['achieve'].keys(): #최초 1회만 작동하게 하기위해 달성여부 검증
        cnt=0
        for i in idstat[now_login]['achieve'].values():
            if i == False: #achieve 딕셔너리에 False개수 카운트
                cnt += 1
        if cnt == 0: #False 개수가 0개이면 업적을 모두 달성했다고 판단.
            print("모든 업적 클리어 !!")
            temp=input("직접 칭호를 만들어보세요!\n!한번 설정하면 변경할 수 없습니다.\n")
            idstat[now_login]['title'].append(temp) #칭호추가
            idstat[now_login]['achieve']['allclear']=True #업적추가
            print(f"커스텀 칭호 : {temp} 획득!!")
def test_allclear():
    for i in idstat[now_login]['achieve'].keys():
        idstat[now_login]['achieve'][i]=True
def change_password():
    checkpw=input("현재 비밀번호 : ")
    if checkpw == idpw[now_login]: #비밀번호 검증
        while True:
            temp_pw=input("변경할 비밀번호 : ") #새비밀번호 설정
            temp_pw2=input("재입력 : ") #새비밀번호 일치확인
            if temp_pw == temp_pw2:
                idpw[now_login]=temp_pw
                print("비밀번호 변경완료.")
                return
            else:
                print("입력하신 두 비밀번호가 다릅니다.")
    else:
        print("비밀번호 오류")
        return
def titleset():
    global idstat
    global now_login
    print("칭호 목록")
    for i in range(0,len(idstat[now_login]["title"])):
        print(i+1,":",idstat[now_login]['title'][i]) #for문으로 현재 보유중인 title 출력
    try: #정수검증 and 인덱스오류 방지(가진 title보다 넘는 수를 입력시 프로그램오류 방지)
        titlecho=int(input())
        idstat[now_login]["now_title"]=idstat[now_login]["title"][titlecho-1]
        print("설정완료.")
        time.sleep(0.5)
    except:
        print("잘못된 번호 선택입니다 (없는 칭호)")
        return

def exp(ex): #기본적인 경험치 지급 함수 매개변수 ex : 지급될 양
    global idstat
    idstat[now_login]['exp'] += ex #idstat 딕셔너리의 exp에 가산
    print("경험치 +"+str(ex)) #지급안내
    time.sleep(0.5)
    
def aexp(ex): #추가지급시 사용 틀은 위 함수랑 동일함.
    global idstat
    idstat[now_login]['exp'] += ex
    print("추가 경험치 +"+str(ex))
    time.sleep(0.5)
    
def saving_data(): #데이터를 저장하기 위한 함수
    global idstat
    global idpw
    with open('idstat.pickle', 'wb') as f: #idstat과 idpw 딕셔너리를 pickle모듈을 통해 바이너리로 저장
        pickle.dump(idstat, f)
    with open('idpw.pickle', 'wb') as f:
        pickle.dump(idpw, f)
def loading_data(): #데이터를 로딩하기 위한 함수
    global idstat
    global idpw
    with open('idstat.pickle', 'rb') as f: #idstat과 idpw딕셔너리를 pickle모듈을 통해 불러들임
        idstat = pickle.load(f)
    with open('idpw.pickle', 'rb') as f:
        idpw = pickle.load(f)
def ranking(): #고침 시발 할렐루야
    texp=[] #total exp
    users=[] #임시적인 유저저장 (id)
    ranku=[] #정렬된 유저닉네임
    ranke=[] #정렬된 경험치
    rankid=[] #정렬된 아이디
    for i in idstat.keys(): #총경험치 계산 반복문
        texp.append((idstat[i]["Lv"]-1)**2+idstat[i]["exp"]) #경험치공식 2n-1 : 총경험치 레벨-1의 제곱, 계산수 texp에 어펜드
        users.append(i) # 해당 경험치에 해당하는 아이디 어펜드, texp와 인덱스를 같게해 동시에 다룰 수 있게 함.
    for i in range(len(texp)): #정렬을 위한 반복문
        temp=0 #최대값을 찾기위한 임시변수
        for i in range(len(texp)): #해당 반복회차의 최대값을 찾는 반복문
            if texp[i] >= temp: #temp보다 큰 총경험치가 있을 경우 temp를 바꿔저장, 해당 id도 같이 임시저장.
                temp=texp[i]
                tempid=users[i]
        tempin=users.index(tempid) #해당 반복회차에서의 최대값의 인덱스를 저장
        ranku.append(idstat[users[tempin]]['nick']) #이후 정렬할 리스트에 순차적으로 어펜드함
        ranke.append(temp)
        rankid.append(tempid)
        del texp[tempin] #해당 반복회차에서의 최대값을 전체 리스트에서 제거, 다음회차를 진행함.
        del users[tempin]
        
    for i in range(len(ranku)): #사용자에게 출력되어 보여질 부분
        combined = f"{idstat[rankid[i]]['now_title']}{ranku[i]}" #칭호와 닉네임 결합변수
        total_exp = ranke[i]
        print(f"{i+1}위 : {combined:<40}총경험치 : {total_exp}") #순위 및 유저, 경험치 출력.
        time.sleep(0.5)
        
def randomgame(): #업다운 게임함수
    global idstat
    while True:
        sel=input("""
1. 게임 시작하기
2. 업다운 설명
3. 나가기\n""")
        if sel == '1':
            random_su=random.randint(1,100) #1~100 사이에 해당하는 정수 랜덤 설정.(정답설정)
            remain_chance=6 #남은횟수 설정 6
            print(random_su) #test용 정답출력 // 최종적으로 삭제할것
            while True: #무한루프 // 남은기회가 없을때 벗어나게함.
                print("남은 기회 :",remain_chance)
                if remain_chance > 0:
                    try: #typeerror 방지용 정수검증
                        enter_su=int(input("수 입력 : "))
                        if enter_su > random_su: #정답이 더 작을때 down출력
                            print("down")
                            remain_chance -= 1
                        elif enter_su < random_su: #정답이 더 클때 up출력
                            print("up")
                            remain_chance -= 1 #이후 남은기회 1차감
                        else:
                            print("정답!") #같을 때 정답
                            exp(3) #경험치 3지급
                            time.sleep(0.5)
                            if remain_chance == 6: #단 한번에 맞추기 추가경험치
                                print("한번에 맞췄어요!")
                                time.sleep(0.5)
                                aexp(10) #추가경험치 10지급
                                time.sleep(0.5)
                            if remain_chance == 6 and idstat[now_login]['achieve']['찍신!(업다운 1번만에 클리어)']==False: #업적용 조건문, 최초성 검증 및 한번에 맞춤 검증
                                idstat[now_login]['achieve']['찍신!(업다운 1번만에 클리어)']=True #업적을 클리어처리
                                print("업적 클리어! : 찍신")
                                time.sleep(0.5)
                                idstat[now_login]['title'].append("찍신") #칭호획득
                                print("칭호 획득 : 찍신")
                                time.sleep(0.5)
                            
                            resel=input("""
1. 다시하기
2. 나가기\n""")
                            if resel == '1':
                                randomgame()
                                return
                            else:
                                return
                    except:
                        print("수를 입력해주세요.")
                else:
                    print("기회가 끝!@~") #기회를 모두 소진했을때
                    exp(1)
                    resel=input("""
1. 다시하기
2. 나가기\n""")
                    if resel == '1':
                        randomgame()
                        return
                    else:
                        return
        elif sel == '2':
            print("0~100까지 랜덤으로 지정된 숫자를 맞히는 게임입니다")
            time.sleep(0.7)
            print("입력한 숫자보다 지정된 숫자가 크면 업, 입력한 숫자보다 지정된 숫자가 작으면 다운이라는 멘트로 지정된 숫자를 추측합니다")
            time.sleep(0.7)
            print("6번 안에 숫자를 맞히세요!")
        else:
            return

def levelup(): #유저의 레벨업을 위한 함수
    global idstat
    global now_login
    global need_exp
    max_lv=100 #최대레벨 설정
    need_exp=idstat[now_login]['Lv']*2-1 #경험치 식
    if idstat[now_login]['Lv'] == max_lv: #최대레벨의 리미트를 위한 조건문
        idstat[now_login]['exp'] = 0
        return
    else:
        while idstat[now_login]['exp'] >= need_exp: #보유 경험치가 필요 경험치를 넘어서있을때 반복,
            idstat[now_login]['exp'] -= need_exp #필요 경험치만큼 보유량삭감
            idstat[now_login]['Lv'] += 1 #레벨업
            need_exp=idstat[now_login]['Lv']*2-1 #필요 경험치 재조정(레벨이 올랐으니)
        return
def buckshot(): #벅샷룰렛 게임함수
    global idstat
    enemylife=3 #플레이어와 적의 피 설정
    mylife=3
    now_turn='me' #턴 설정을 위한 변수 (시작시 기본으로 플레이어턴)
    while True:
        shots=random.randint(3,6) #장전할 총알개수 랜덤지정
        shotlist=[] #탄창리스트
        for i in range(shots): #탄창을 위한 반복문
            shot=random.randint(0,1) # 0을 공포탄 1을 실탄으로 설정
            shotlist.append(shot) #탄창에 넣음
        print("총 탄:",len(shotlist))
        sil=shotlist.count(1) #실탄개수 카운트
        gong=shotlist.count(0) #공포탄개수 카운트
        print("실탄 :",sil)
        print("공포탄 :",gong) #게임을 위해 총개수와 공포탄 실탄개수 출력
        for i in range(len(shotlist)): #잔여 총탄만큼 반복
            time.sleep(0.5)
            print("적 피", enemylife)
            time.sleep(0.5)
            print("내 피", mylife) #현재 스코어 출력
            now_shot=shotlist.pop(0) #제일 앞 인덱스에 해당하는 값을 pop하여 값을 뽑으며 리스트에서 삭제
            if enemylife == 0: #적의 패배 감지용
                print("승리")
                exp(3) #경험치지급
                if mylife == 3: #한발도 맞지 않고 승리시
                    print("완벽한 승리!")
                    aexp(10) #추가경험치 지급
                    if idstat[now_login]['achieve']["타고난 승부사(벅샷룰렛에서 피해를 입지않고 클리어)"] == False: #최초감지
                        print("타고난 승부사 업적 달성.")
                        time.sleep(0.5)
                        idstat[now_login]['achieve']["타고난 승부사(벅샷룰렛에서 피해를 입지않고 클리어)"] = True #업적클리어
                        print("칭호획득 : 승부사")
                        time.sleep(0.5)
                        idstat[now_login]['title'].append("승부사") #칭호획득
                return #게임 종료에 따라 함수종료(반환)
            if mylife == 0: #나의 패배 감지
                print("패배..")
                exp(1)
                return #함수종료
            if now_turn == 'me': #턴 감지용
                time.sleep(0.5)
                print("본인턴.")
                shot_select=input("1. 상대에게 쏘기\n2. 자신에게 쏘기\n")
                if shot_select == '1' and now_shot == 0: #쏘는 대상 및 현재 총알에 따른 4가지 경우의수
                    time.sleep(0.5)
                    print("공포탄.\n턴이 넘어갑니다.\n")
                    now_turn='you' #상대에게 쏨에 따라 턴넘김.
                    if len(shotlist)==0: #총알 전부 소진시 재장전
                        time.sleep(0.5)
                        print("총알 소진.")
                        time.sleep(0.5)
                        print("재장전합니다.")
                    continue #총알 소진 후 뒤 명령어들이 시행되지 않게 컨티뉴
                elif shot_select == '1' and now_shot == 1:
                    time.sleep(0.5)
                    print("실탄.\n적의 피 -1\n턴이 넘어갑니다.\n")
                    enemylife -= 1
                    now_turn='you'
                    if len(shotlist)==0:
                        time.sleep(0.5)
                        print("총알 소진.")
                        time.sleep(0.5)
                        print("재장전합니다.")
                    continue
                elif shot_select =='2' and now_shot == 1:
                    time.sleep(0.5)
                    print("실탄.\n나의 피 -1\n턴이 넘어갑니다.\n")
                    mylife -= 1
                    now_turn='you'
                    if len(shotlist)==0:
                        time.sleep(0.5)
                        print("총알 소진.")
                        time.sleep(0.5)
                        print("재장전합니다.")
                    continue
                elif shot_select =='2' and now_shot == 0:
                    time.sleep(0.5)
                    print("공포탄.\n턴을 계속합니다.\n")
                    now_turn='me' #자신에게 쏘고, 공포탄이므로 턴유지
                    if len(shotlist)==0:
                        time.sleep(0.5)
                        print("총알 소진.")
                        time.sleep(0.5)
                        print("재장전합니다.")
                    continue
            elif now_turn == 'you': #적의턴 감지
                time.sleep(0.5)
                print("적의 턴.")
                enemysel=random.randint(1,2) #적의 선택을 랜덤으로 정하기 1 : 상대 2 : 자신에게 쏘기
                if enemysel == 1 and now_shot == 0: #위와 동일.
                    time.sleep(0.5)
                    print("나에게 쏨.")
                    time.sleep(0.5)
                    print("공포탄.\n턴이 넘어갑니다.\n")
                    now_turn='me'
                    if len(shotlist)==0:
                        time.sleep(0.5)
                        print("총알 소진.")
                        time.sleep(0.5)
                        print("재장전합니다.")
                    continue
                elif enemysel == 1 and now_shot == 1:
                    time.sleep(0.5)
                    print("나에게 쏨.")
                    time.sleep(0.5)
                    print("실탄.\n나의 피 -1\n턴이 넘어갑니다.\n")
                    now_turn='me'
                    mylife -= 1
                    if len(shotlist)==0:
                        time.sleep(0.5)
                        print("총알 소진.")
                        time.sleep(0.5)
                        print("재장전합니다.")
                    continue
                elif enemysel == 2 and now_shot == 1:
                    time.sleep(0.5)
                    print("스스로 쏨.")
                    time.sleep(0.5)
                    print("실탄.\n적의 피 -1\n턴이 넘어갑니다.\n")
                    now_turn='me'
                    enemylife -= 1
                    if len(shotlist)==0:
                        time.sleep(0.5)
                        print("총알 소진.")
                        time.sleep(0.5)
                        print("재장전합니다.")
                    continue
                elif enemysel == 2 and now_shot == 0:
                    time.sleep(0.5)
                    print("스스로 쏨.")
                    time.sleep(0.5)
                    print("공포탄.\n턴을 계속합니다.\n")
                    now_turn='you'
                    if len(shotlist)==0:
                        time.sleep(0.5)
                        print("총알 소진.")
                        time.sleep(0.5)
                        print("재장전합니다.")
                    continue
def baseballgame(): #야구게임 함수
    global idstat
    num=[1,2,3,4,5,6,7,8,9]
    ans=[] #정답리스트
    cnt=1 #시도 횟수 카운트변수
    for i in range(4): #정답만들기 반복문
        numran=random.randrange(0,len(num)) #남아있는 num중 랜덤선택
        ans.append(num[numran]) #정답에 추가
        num.remove(num[numran]) #num에서 제거 (중복 숫자 방지)
    print(ans) #test용 정답출력 // 최종에서 삭제할것
    print("포기하려면 포기 입력")
    print("4자리 수를 골라줘!\n")
    while True:
        print("%d번째 시도"%cnt)
        enter_num=input()
        if "포기" in enter_num: #포기용
            return
        enter_num_li=list(str(enter_num)) #입력된 수를
        strike=0
        ball=0
        if len(enter_num_li) != 4:
            print("4자리수를 입력해줘")
            continue
        for i in range(4):
            try:
                if int(enter_num_li[i])== ans[i]:
                    strike += 1
                elif int(enter_num_li[i]) in ans:
                    ball += 1
            except:
                print("수를 입력해줘 !")
                break
            
        if strike == 4: #정답감지
            print("정답!!")
            exp(5)
            if cnt <= 5:
                print("빠른 클리어!")
                aexp(15)
                if idstat[now_login]['achieve']["빠른 클리어(야구게임에서 5번 시도 내 클리어)"]==False:
                    print("업적클리어 : 빠른 클리어")
                    idstat[now_login]['achieve']["빠른 클리어(야구게임에서 5번 시도 내 클리어)"]=True
                    time.sleep(0.5)
                    print("칭호 획득 : 메이저리거")
                    idstat[now_login]['title'].append("메이저리거")
            return
        if strike == 0 and ball == 0:
            print("노볼 노스트라이크!")
        else:
            print("%d볼 %d스트라이크!"%(ball, strike))
        cnt += 1 #시도횟수 +1
            

def highlow(): #하이로우 게임함수
    global idstat
    highlow_ac={"high":False, "low" : False, "middle":False} #업적용 딕셔너리

    print("하이로우에 온것을 환영해\n")
    time.sleep(0.5)
    print("너와 나는 각각 1~100사이에 임의의 수를 하나씩 뽑게될거야.")
    time.sleep(0.5)
    print("하이는 크면, 미들은 50에 가까우면, 로우는 작으면 승리야!")
    time.sleep(0.5)
    print("그럼 뭘 할래 ?")
    time.sleep(0.5)
    while True:
        if idstat[now_login]["achieve"]["뭘해도(하이로우에서 하이, 로우, 미들 전부 승리)"]==False: #최초검증
            Tcnt = 0 #하이 로우 미들 몇종류 클리어했는지 카운트변수
            for value in highlow_ac.values():
                if value == True: #클리어시
                    Tcnt +=1 #카운트+1
            if Tcnt == 3: #모두 클리어시 : 카운트 = 3
                print("업적달성 : 뭘해도")
                time.sleep(0.5)
                idstat[now_login]["achieve"]["뭘해도(하이로우에서 하이, 로우, 미들 전부 승리)"] = True
                print("칭호획득 : Victory")
                time.sleep(0.5)
                idstat[now_login]['title'].append("Victory")
        hcho=input("1.하이\n2.미들\n3.로우\n\n나가려면 아무거나 입력해!\n") #종목선택
        dealer=random.randrange(1,101) 
        me=random.randrange(1,101) #상대와 나의 수 랜덤설정
        if hcho == '1': #하이룰
            time.sleep(0.5)
            print("딜러의 수 :", dealer)
            time.sleep(1)
            print("당신의 수 :", me)
            time.sleep(0.5)
            if dealer == me: #비교 조건문
                print("이런 ! 비겼어!")
                exp(3)
            elif dealer > me:
                print("야호! 내가 이겼다!")
                exp(1)
            else:
                print("이런 내가 졌네..")
                exp(5)
                highlow_ac["high"]=True #업적용 하이 클리어
        elif hcho == '2': #미들룰
            time.sleep(0.5)
            print("딜러의 수 :", dealer)
            time.sleep(1)
            print("당신의 수 :", me)
            time.sleep(0.5)
            dealer -= 50
            me -= 50 #50과의 차이 연산
            if dealer < 0:
                dealer = -dealer
            if me < 0:
                me = -me #절대값 작업
            print("딜러와 50의 차 :", dealer)
            print("나와 50의 차 :", me)
            if dealer == me: #비교 조건문
                print("이런 ! 비겼어!")
                exp(3)
            elif dealer < me:
                print("야호! 내가 이겼다!")
                exp(1)
            else:
                print("이런 내가 졌네..")
                exp(5)
                highlow_ac["middle"]=True #업적용 클리어체크
        elif hcho == '3': #로우룰
            time.sleep(0.5)
            print("딜러의 수 :", dealer)
            time.sleep(1)
            print("당신의 수 :", me)
            time.sleep(0.5)
            if dealer == me: #비교 조건문
                print("이런 ! 비겼어!")
                exp(1)
            elif dealer < me:
                print("야호! 내가 이겼다!")
                exp(3)
            else:
                print("이런 내가 졌네..")
                exp(5)
                highlow_ac["low"]=True #업적용 로우 클리어체크
        else:
            print("잘가!") #1,2,3 이외 입력시 종료
            return
    

def roulette():
    global idstat
    print("룰렛을 시작할게 !")
    chonum=[] #나의 선택 빈 리스트
    ans=random.randint(1,36) #정답설정
    print(ans)
    cho=input('''어디에 걸래?
              1. 홀수 (경험치3)
              2. 짝수 (경험치3)
              3. 1~18 (경험치3)
              4. 19~36 (경험치3)
              5. 1~12 (경험치10)
              6. 13~24 (경험치10)
              7. 25~36 (경험치10)
              8. 내가 고를래 ! (경험치1000)
              ''')
    if cho =='1':
        for i in range(18):
            chonum.append(2*i-1) #홀수를 나의 선택리스트에 추가
    if cho == '2':
        for i in range(18):
            chonum.append(2*i) #짝수를 나의 선택리스트에 추가
    if cho == '3':
        for i in range(1,19): #해당하는 수를 나의 선택리스트에 추가
            chonum.append(i)
    if cho =='4':
        for i in range(19,37):
            chonum.append(i)
    if cho == '5':
        for i in range(1,13):
            chonum.append(i)
    if cho == '6':
        for i in range(13,25):
            chonum.append(i)
    if cho == '7':
        for i in range(25,37):
            chonum.append(i)
    if cho == '8':
        time.sleep(0.5)
        chonum.append(int(input("좋아! 네가 골라봐!\n")))
    print("이제 돌릴게")
    time.sleep(0.5)
    for i in range(20):                             #시각적 효과를 위한 반복문 (룰렛이 돌아가는 것처럼 보이게)
        print("            ", random.randint(1,36))
        time.sleep(0.1)
    print("            ", random.randint(1,36))
    time.sleep(0.3)
    print("            ", random.randint(1,36))
    time.sleep(0.5)
    print("            ", random.randint(1,36))
    time.sleep(0.7)
    print(ans,"!!")    
    if ans in chonum:
        print("성공이야!")
        if cho == "1" or cho == "2" or cho == "3" or cho == "4": # 각 배수에 따른 경험치 지급
            exp(3)
        if cho == "5" or cho == "6" or cho == "7":
            exp(10)
        if cho == "8":
            exp(1000)
    else:
        print("실패했어 ㅜㅜ")
    print("계속할래 ?")
    recho=input("1. 예\n2. 아니요\n") #재진행선택
    if recho == '1':
        roulette() #재귀함수
    else:
        print("잘가!") # 1 외에 반환
        return
#메인함수 영역
idpw={} #최초 실행을 위한 빈 딕셔너리
idstat={}
now_login='' 
loading_data() #데이터 인식후 딕셔너리 채움
gamelist=["업다운 숫자맞추기", "벅샷룰렛","야구게임", "하이로우","룰렛"]
#_art는 사용자에게 시각적 안내용 아트
login_art = """
    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
      로그인화면                                 로그인해주세요.
    ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
    
    
    　　　　　　 
     　　　1. 로그인 　　　2. 회원가입 　      3.종료   
    　　　　   
        """
main_art="""
    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
      메인화면                               %s  %s님
    ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿


"""
set_art = """
    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
      설정화면                               %s  %s님
    ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
    
    
     1. 내 정보   2. 비밀번호 변경  3. 닉네임 변경    4.업적 설정
     
     5. 로그아웃  6. 계정삭제  7.종료
       """
stat_art = """
    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
        {} {}님의 정보
    ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
    
    레벨 : {}
    경험치 : {}  /  {}
    업적 : {}
    최근 검색 기록 : 
       """

game_art="""
    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
      게임화면                               %s  %s님
    ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿    
    
    
"""

        
while True:
    saving_data() #진행상태 저장
    loading_data() #로드
    if now_login == '': #현재 로그인 x검증
        while True:
            print(login_art)
            loginmenu=input()
            if loginmenu=='1' or loginmenu == '로그인': #선택에 따라 로그인 회원가입 종료
                login()
                time.sleep(0.5)
                break
            elif loginmenu=='2' or loginmenu == '회원가입':
                register()
                time.sleep(0.5)
            elif loginmenu == '3' or loginmenu == '종료':
                sys.exit("프로그램을 종료합니다.")
            else:
                print("올바른 메뉴를 골라주세요.")
    else:
        saving_data() #데이터 저장
        loading_data() #로드
        levelup() #레벨업 검증
        allclear() #업적 올클리어 검증
        time.sleep(1)
        ach_="\n\t   ".join(list(map(achmap, idstat[now_login]['achieve'].items()))) #업적표시용 변수
        print(main_art%(idstat[now_login]["now_title"], idstat[now_login]['nick'])) #화면에 칭호와 닉네임 출력
        print('''
1. 설정
2. 검색
3. 게임
4. 랭킹''')
        while True: #무한루프
            mainmenu=input()
            if "설정" in mainmenu or "게임" in mainmenu or "검색" in mainmenu or "랭킹" in mainmenu or\
                "1" in mainmenu or "2" in mainmenu or "3" in mainmenu or "4" in mainmenu or "test" in mainmenu: #메뉴검증
                break #올바른 메뉴 선택이 메뉴선택 반복문 벗어남
            else:
                print("잘 모르겠어요")
        if "설정" in mainmenu or "1" in mainmenu:
            print(set_art%(idstat[now_login]["now_title"], idstat[now_login]['nick']))
            setmenu=input()
            if setmenu == '1':
                print(stat_art.format(idstat[now_login]["now_title"],idstat[now_login]['nick'],idstat[now_login]['Lv'],idstat[now_login]['exp'],need_exp,ach_))
                choo = input("돌아가시려면 아무거나 입력하세요\n")
            elif setmenu == '2':
                change_password()
            elif setmenu == '3':
                change_nick()
            elif setmenu == '5':
                logout()
            elif setmenu == '7':
                print("프로그램 종료")
                break
            elif setmenu == '4':
                titleset()
            elif setmenu == '6':
                remove_id()
            elif setmenu == '전부지워라': #테스트용, db지우기
                idstat.clear()
                idpw.clear()
                now_login=''
                print("DB초기화")
            else:
                a=1
        elif "올클" in mainmenu:
            test_allclear()
        elif "검색" in mainmenu or "2" in mainmenu:
            pass
        elif "랭킹" in mainmenu or "4" in mainmenu:
            ranking()
        elif "게임" in mainmenu or "3" in mainmenu:
            print(game_art%(idstat[now_login]["now_title"], idstat[now_login]['nick']))
            time.sleep(0.7)
            print("게임파트에 온 걸 환영해!")
            time.sleep(0.7)
            print("할 수 있는 게임이 궁금하다면 도움말을 입력해봐!")
            time.sleep(0.7)
            print("메인화면으로 돌아가려면 나가기를 입력해줘!")
            while True:
                saving_data() #데이터 저장
                loading_data() #로드
                levelup() #레벨업 검증
                allclear() #업적 올클리어 검증
                time.sleep(1)
                print(game_art%(idstat[now_login]["now_title"], idstat[now_login]['nick']))
                for i in range(len(gamelist)):
                    print(f"{i+1}. {gamelist[i]}")
                while True:
                    gamemenu=input()
                    if "나가" in gamemenu:
                        break
                    if "업다운" in gamemenu or "벅샷" in gamemenu or "룰렛" in gamemenu or "하이로우" in gamemenu \
                        or "야구" in gamemenu or"랭킹" in gamemenu or "1" in gamemenu or "2" in gamemenu or "3" in gamemenu\
                            or "4" in gamemenu or "5" in gamemenu:
                        break
                    else:
                        print("지원하지 않는 게임입니다.")
                if "나가" in gamemenu:
                    break
                if "업다운" in gamemenu or "1" in gamemenu:
                    randomgame()
                elif "ex" in gamemenu: #test용 경험치지급 // 최종삭제
                    idstat[now_login]['exp'] += 3
                elif "벅샷" in gamemenu or "2" in gamemenu:
                    time.sleep(0.5)
                    print("벅샷룰렛에 오신 것을 환영합니다.")
                    time.sleep(0.5)
                    while True: #무한루프
                        bucksel=input("1. 벅샷룰렛 시작하기\n2. 벅샷룰렛 설명듣기\n3. 나가기\n") #선택변수
                        if bucksel == '1':
                            buckshot() #룰렛함수로 이동
                            break #메인으로 가기위한 break
                        elif bucksel == '2':
                            time.sleep(0.7)
                            print("벅샷 룰렛은 죽음의 룰렛게임 입니다!")
                            time.sleep(0.7)
                            print("한 탄창은 3개에서 6개가 랜덤하게 설정됩니다.")
                            time.sleep(0.7)
                            print("탄창에는 공포탄 혹은 실탄이 들어갑니다.")
                            time.sleep(0.7)
                            print("실탄이라고 생각하면 적에게, 공포탄이라고 생각하면 스스로 쏴보세요!")
                            time.sleep(0.7)
                            print("스스로 공포탄을 쏜다면 계속해서 턴을 유지합니다!!")
                            time.sleep(0.7)
                            print("물론 선택의 책임은 오로지 본인에게 있습니다..")
                            time.sleep(0.7)
                            print("적이 나를 죽이기 전에 적을 죽여버리세요!")
                            time.sleep(0.7)
                            print("그럼 행운을 빕니다....")
                        else:
                            print("메인메뉴로 돌아갑니다.")
                            time.sleep(0.5)
                            break
                elif "야구" in gamemenu or "3" in gamemenu:
                    time.sleep(0.5)
                    print("야구게임에 오신 것을 환영합니다.")
                    time.sleep(0.5)
                    while True: #무한루프
                        yasel=input("1. 시작하기\n2. 설명듣기\n3. 나가기\n") #선택변수
                        if yasel == '1':
                            baseballgame() #룰렛함수로 이동
                            break #메인으로 가기위한 break
                        elif yasel == '2':
                            print("야구게임은 랜덤한 4자리 수를 맞추는 게임입니다")
                            time.sleep(0.7)
                            print("그 수가 정답에 있다면 볼, 위치까지 맞다면 스트라이크입니다")
                            time.sleep(0.7)
                            print("예를 들어 정답이 1234일 경우 3456은 2볼 0스트라이크입니다.")
                            time.sleep(0.7)
                            print("1324라면 2볼 2스트라이크겠죠!")
                            time.sleep(0.7)
                        else:
                            print("메인메뉴로 돌아갑니다.")
                            time.sleep(0.5)
                            break
                elif "하이로우" in gamemenu or "4" in gamemenu:
                    highlow()
                elif "룰렛" in gamemenu or "5" in gamemenu:
                    time.sleep(0.5)
                    print("룰렛에 오신 것을 환영합니다.")
                    time.sleep(0.5)
                    while True: #무한루프
                        roulsel=input("1. 룰렛 시작하기\n2. 룰렛 설명듣기\n3. 나가기\n") #선택변수
                        if roulsel == '1':
                            roulette() #룰렛함수로 이동
                            break #메인으로 가기위한 break
                        elif roulsel == '2':
                            print("룰렛은 지정하신 번호가 나오면 당첨하는 간단한 게임입니다.")
                        else:
                            print("메인메뉴로 돌아갑니다.")
                            time.sleep(0.5)
                            break
                elif "랭킹" in gamemenu:
                    ranking()