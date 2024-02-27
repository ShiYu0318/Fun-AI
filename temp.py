# #----------------------------------------------------------------------------------------------------------------------------------



    ##########  to do  ##########
    def __get_obs(self, scene_info):      


        power = scene_info["power"]
        power_var = scene_info["power"] - self.pre_scene_info["power"]
        score_var = scene_info["score"] - self.pre_scene_info["score"]
        is_hit = scene_info["competitor_info"][0]["lives"] - self.pre_scene_info["competitor_info"][0]["lives"] < 0

        my_x = scene_info["x"]
        my_y = scene_info["y"]
        pre_my_x = self.pre_scene_info["x"]
        pre_my_y = self.pre_scene_info["y"]
        bs_x = scene_info["bullet_stations_info"][0]["x"]
        bs_y = scene_info["bullet_stations_info"][0]["y"]


        to_bs_x = bs_x - my_x
        to_bs_y = bs_y - my_y

        Grid_px = 5


        if abs(bs_x - my_x) < Grid_px:
            Target_x = "CORRECT"
        elif bs_x - my_x > Grid_px:
            Target_x = "RIGHT"        
        elif bs_x - my_x < -Grid_px:
            Target_x = "LEFT"
        else:
            Target_x = "NONE"
        
        if abs(bs_y - my_y) < Grid_px:
            Target_y = "CORRECT"
        elif bs_y - my_y > Grid_px:
            Target_y = "DOWN"
        elif bs_y - my_y < -Grid_px:
            Target_y = "UP"        
        else:
            Target_y = "NONE"

        if my_x - pre_my_x > Grid_px:
            Vector_x = "GOING_RIGHT"
        elif my_x - pre_my_x < -Grid_px:
            Vector_x = "GOING_LEFT"
        else:
            Vector_x = "ZERO"
        
        if my_y - pre_my_y > Grid_px:
            Vector_y = "GOING_DOWN"
        elif my_y - pre_my_y < -Grid_px:
            Vector_y = "GOING_UP"
        else:
            Vector_y = "ZERO" 



        self.pre_scene_info = scene_info    

        observation = {
                "power" : power , "power_var" : power_var,
                "score_var" : score_var, "is_hit" : is_hit,
                # "my_x" : my_x, "my_y" : my_y,
                # "pre_my_x" : pre_my_x, "pre_my_y" : pre_my_y, 
                # "bs_x" : bs_x, "bs_y" : bs_y,
                # "to_bs_x" : to_bs_x , "to_bs_y" : to_bs_y,
                "Target_x" : Target_x , "Target_y" : Target_y,
                "Vector_x" : Vector_x , "Vector_y" : Vector_y
                # "cp_x" : cp_x, "cp_y" : cp_y,
        }
        
        return observation


#----------------------------------------------------------------------------------------------------------------------------------

    ##########  to do  ##########
    def __get_reward(self, observation):        
        
        reward = 0        
        
        # Face = observation["Face"]
        power = observation["power"]
        power_var = observation["power_var"]
        score_var = observation["score_var"]
        is_hit = observation["is_hit"]

        # my_x = observation["my_x"]
        # my_y = observation["my_y"]
        # pre_my_x = observation["pre_my_x"]
        # pre_my_y = observation["pre_my_y"]
        # cp_x = observation["cp_x"]
        # cp_y = observation["cp_y"]
        # bs_x = observation["bs_x"]
        # bs_y = observation["bs_y"]
        # to_bs_x = observation["to_bs_x"]
        # to_bs_y = observation["to_bs_y"]
        # pre_to_bs_x = observation["pre_to_bs_x"]
        # pre_to_bs_y = observation["pre_to_bs_y"]
        Target_x = observation["Target_x"]
        Target_y = observation["Target_y"]
        Vector_x = observation["Vector_x"]
        Vector_y = observation["Vector_y"]

        Tv_map = {
            "CORRECT" : "ZERO",
            "RIGHT" : "GOING_RIGHT",
            "LEFT" : "GOING_LEFT",
            "UP" : "GOING_UP",
            "DOWN" : "GOING_DOWN",
            "NONE" : "NONE"
        }
        # to_bs_dis = observation["to_bs_dis"]
        # pre_to_bs_dis = observation["pre_to_bs_dis"]

        if score_var != 0: reward += 1500
        if is_hit: reward += 2000
        
        get_power = False

        # if power == 0:
        if power_var > 0: 
            get_power = True
            reward += 3000

        if Target_x == "CORRECT": reward += 400
        if Target_y == "CORRECT": reward += 400

        if Tv_map[Target_x] == Vector_x:
            reward += 500
        else:
            reward -= 100

        if Tv_map[Target_y] == Vector_y:
            reward += 500
        else:
            reward -= 100
        # Grid_px = 10

        # if abs(bs_x - my_x) < Grid_px:
        #     if bs_y - my_y < 0 and Vector_y == "GOING_UP":
        #         reward += 100
        #     elif bs_y - my_y > 0 and Vector_y == "GOING_DOWN":
        #         reward += 100
        #     else: reward -= 50
        # elif abs(bs_y - my_y) < Grid_px:
        #     if bs_x - my_x < 0 and Vector_x == "GOING_RIGHT":
        #         reward += 100
        #     elif bs_y - my_y > 0 and Vector_x == "GOING_LEFT":
        #         reward += 100
        #     else: reward -= 50
        # else:
        #     if bs_y - my_y < 0 and Vector_y == "GOING_UP":
        #         reward += 100
        #     elif bs_y - my_y > 0 and Vector_y == "GOING_DOWN":
        #         reward += 100
        #     else: reward -= 50






        # if to_bs_dis < pre_to_bs_dis:
        #     reward += (pre_to_bs_dis - to_bs_dis) * 10
        # elif to_bs_dis == pre_to_bs_dis:
        #     reward -= 8
        # else:
        #     reward -= (to_bs_dis - pre_to_bs_dis) * 5

            # if to_bs_x < pre_to_bs_x:
            #     reward += 500
            # else: reward -= 200            
            
            # if to_bs_y < pre_to_bs_y:
            #     reward += 500
            # else: reward -= 200
        # else:
        #     if power_var < 0:
        #         if score_var > 0: reward += 500
        #         else: reward -= 500

        #     if abs(my_y - cp_y) < 50:
        #         reward += 500
        #     else:
        #         reward -= 200

        #     if abs(my_x - cp_x) < 250:
        #         reward += 500
        #     else:
        #         reward -= 200


        # \n to_bs_dis : {to_bs_dis} || pre_to_bs_dis : {pre_to_bs_dis} ||
        # 
        print(f"is_hit ? {is_hit} || get score ? {score_var} || power : {power} || get_power ? {get_power} ||  reward : {reward}\n")
        return reward
    
#----------------------------------------------------------------------------------------------------------------------------------




        # FaceMap = { 0: "LEFT" ,45: "DOWNLEFT" ,90: "DOWN" ,135:"DOWNRIGHT"
#         #             ,180:"RIGHT" ,225:"UPRIGHT" ,270:"UP" ,315:"UPLEFT", 360: "LEFT"}

    
#         # Face = {"Face": FaceMap[abs(scene_info["angle"])]}
#         # Tank_pos = [scene_info["x"], scene_info["y"]]




#         # return OrderedDict([('Face', face), 
#         #                     ('Tank_pos', Tank_pos)])        
        
# #----------------------------------------------------------------------------------------------------------------------------------

#         # FaceMap = { 0: "LEFT" ,45: "DOWNLEFT" ,90: "DOWN" ,135:"DOWNRIGHT"
#         #             ,180:"RIGHT" ,225:"UPRIGHT" ,270:"UP" ,315:"UPLEFT", 360: "LEFT"}

#         # Grid_px = 10

        
#         # Tank_BS_dis = math.sqrt((my_x - cp_x) * (my_x - cp_x) + (my_y - cp_y) * (my_y - cp_y))
#         # pre_Tank_BS_dis = math.sqrt((pre_my_x - pre_cp_x) * (pre_my_x - pre_cp_x) + (pre_my_y - pre_cp_y) * (pre_my_y - pre_cp_y))
#         # Tank_BS_dis_var = Tank_BS_dis - pre_Tank_BS_dis
        
        
#         # if abs(my_x - cp_x) < 240:
#         #     Target_x = "CORRECT"
#         # elif my_x - cp_x >= 240:
#         #     Target_x = "LEFT"
        
#         # if abs(my_y - cp_y) < Grid_px:
#         #     Target_y = "CORRECT"
#         # elif my_y - cp_y >= Grid_px:
#         #     Target_y = "UP"
#         # elif cp_y - my_y >= Grid_px:    
#         #     Target_y = "DOWN"        


#         # if abs(my_x - pre_my_x) < Grid_px:
#         #     Vector_x = "ZERO"
#         # elif my_x - pre_my_x >= Grid_px:
#         #     Vector_x = "GOING_RIGHT"
#         # elif pre_my_x - my_x >= Grid_px:
#         #     Vector_x = "GOING_LEFT"
        
#         # if (my_y - pre_my_y) < Grid_px:
#         #     Vector_y = "ZERO"        
#         # elif my_y - pre_my_y >= Grid_px:
#         #     Vector_y = "GOING_DOWN"
#         # elif pre_my_y - my_y >= Grid_px:
#         #     Vector_y = "GOING_UP"
        
#         # # if abs(my_x - bs_x) < Grid_px:
#         # #     bullet_stations_target_x = "CORRECT"
#         # # elif my_x - bullet_stations_x >= Grid_px:
#         # #     bullet_stations_target_x = "LEFT"   
#         # # elif bullet_stations_x - my_x >= Grid_px:
#         # #     bullet_stations_target_x = "RIGHT"   
        
#         # # if abs(scene_info["y"] - bullet_stations_y) < Grid_px:
#         # #     bullet_stations_target_y = "CORRECT"
#         # # elif scene_info["y"] - bullet_stations_y >= Grid_px:
#         # #     bullet_stations_target_y = "UP"
#         # # elif bullet_stations_y - scene_info["y"] >= Grid_px:
#         # #     bullet_stations_target_y = "DOWN"
        




# #----------------------------------------------------------------------------------------------------------------------------------


#         # power = scene_info["power"]
#         # power_var = scene_info["power"] - self.pre_scene_info["power"]
#         # score_var = scene_info["score"] - self.pre_scene_info["score"]
#         # is_hit = scene_info["competitor_info"][0]["lives"] - self.pre_scene_info["competitor_info"][0]["lives"] < 0

#         # my_x = scene_info["x"]
#         # my_y = scene_info["y"]
#         # pre_my_x = self.pre_scene_info["x"]
#         # pre_my_y = self.pre_scene_info["y"]
#         # bs_x = scene_info["bullet_stations_info"][0]["x"]
#         # bs_y = scene_info["bullet_stations_info"][0]["y"]


#         # Tank_bs_x = bs_x - pre_my_x
#         # Tank_bs_y = bs_y - pre_my_y

#         # # Determine the region based on the sum and difference of the relative coordinates
#         # if Tank_bs_x + Tank_bs_y > 0:
#         #     if Tank_bs_x - Tank_bs_y > 0:
#         #         bs_direction = 1  # Right
#         #     else:
#         #         bs_direction = 2  # Up
#         # else:
#         #     if Tank_bs_x - Tank_bs_y > 0:
#         #         bs_direction = 4  # Down
#         #     else:
#         #         bs_direction = 3  # Left

#         # # if abs(Tank_bs_x) < revision and abs(Tank_bs_x) < revision:
#         # #     bs_direction = "CORRECT"
#         # # elif abs(Tank_bs_x) < revision and Tank_bs_y < -revision:
#         # #     bs_direction = "UP"
#         # # elif abs(Tank_bs_x) < revision and Tank_bs_y > revision:
#         # #     bs_direction = "DOWN"
#         # # elif abs(Tank_bs_y) < revision and Tank_bs_x < -revision:
#         # #     bs_direction = "LEFT"
#         # # elif abs(Tank_bs_y) < revision and Tank_bs_x > revision:
#         # #     bs_direction = "RIGHT"
        
#         # # elif Tank_bs_y > 0 and Tank_bs_y >= abs(Tank_bs_x):
#         # #     bs_direction = "UP"  
#         # # elif Tank_bs_y < 0 and Tank_bs_y >= abs(Tank_bs_x):
#         # #     bs_direction = "DOWN"
#         # # elif Tank_bs_x < 0 and Tank_bs_x >= abs(Tank_bs_y):
#         # #     bs_direction = "LEFT"
#         # # elif Tank_bs_x > 0 and Tank_bs_x >= abs(Tank_bs_y):
#         # #     bs_direction = "RIGHT"


#         # my_var_x = my_x - pre_my_x
#         # my_var_y = my_y - pre_my_y



#         # if my_var_x + my_var_y > 0:
#         #     if my_var_x - my_var_y > 0:
#         #         my_direction = 1  # Right
#         #     else:
#         #         my_direction = 2  # Up
#         # else:
#         #     if my_var_x - my_var_y > 0:
#         #         my_direction = 4  # Down
#         #     else:
#         #         my_direction = 3  # Left
#         # # if my_var_y > 0 and my_var_y >= abs(my_var_x):
#         # #     my_direction = "UP"  
#         # # elif my_var_y < 0 and my_var_y >= abs(my_var_x):
#         # #     my_direction = "DOWN"
#         # # elif my_var_x < 0 and my_var_x >= abs(my_var_y):
#         # #     my_direction = "LEFT"
#         # # elif my_var_x > 0 and my_var_x >= abs(my_var_y):
#         # #     my_direction = "RIGHT"







# #----------------------------------------------------------------------------------------------------------------------------------



#     ##########  to do  ##########
#     def __get_obs(self, scene_info):      


#         power = scene_info["power"]
#         power_var = scene_info["power"] - self.pre_scene_info["power"]
#         score_var = scene_info["score"] - self.pre_scene_info["score"]
#         is_hit = scene_info["competitor_info"][0]["lives"] - self.pre_scene_info["competitor_info"][0]["lives"] < 0

#         my_x = scene_info["x"]
#         my_y = scene_info["y"]
#         pre_my_x = self.pre_scene_info["x"]
#         pre_my_y = self.pre_scene_info["y"]
#         cp_x = scene_info["competitor_info"][0]["x"]
#         cp_y = scene_info["competitor_info"][0]["y"]
#         bs_x = scene_info["bullet_stations_info"][0]["x"]
#         bs_y = scene_info["bullet_stations_info"][0]["y"]


#         to_bs_x = abs(bs_x - my_x)
#         to_bs_y = abs(bs_y - my_y) 
#         pre_to_bs_x = abs(bs_x - pre_my_x)
#         pre_to_bs_y = abs(bs_y - pre_my_y)

#         to_bs_dis = math.sqrt(to_bs_x * to_bs_x + to_bs_y * to_bs_y)
#         pre_to_bs_dis = math.sqrt(pre_to_bs_x * pre_to_bs_x + pre_to_bs_y * pre_to_bs_y)

#         self.pre_scene_info = scene_info    

#         observation = {
#                 "power" : power , "power_var" : power_var,
#                 "score_var" : score_var, "is_hit" : is_hit,
#                 "to_bs_x" : to_bs_x , "to_bs_y" : to_bs_y,
#                 "pre_to_bs_x" : pre_to_bs_x , "pre_to_bs_y" : pre_to_bs_y,
#                 "my_x" : my_x, "my_y" : my_y,
#                 "pre_my_x" : pre_my_x, "pre_my_y" : pre_my_y, 
#                 "cp_x" : cp_x, "cp_y" : cp_y,
#                 "bs_x" : bs_x, "bs_y" : bs_y,
#                 "to_bs_dis" : to_bs_dis , "pre_to_bs_dis" : pre_to_bs_dis
#         }
        
#         return observation


# #----------------------------------------------------------------------------------------------------------------------------------

#     ##########  to do  ##########
#     def __get_reward(self, observation):        
        
#         reward = 0        
        
#         # Face = observation["Face"]
#         power = observation["power"]
#         power_var = observation["power_var"]
#         score_var = observation["score_var"]
#         is_hit = observation["is_hit"]

#         my_x = observation["my_x"]
#         my_y = observation["my_y"]
#         # pre_my_x = observation["pre_my_x"]
#         # pre_my_y = observation["pre_my_y"]
#         cp_x = observation["cp_x"]
#         cp_y = observation["cp_y"]
#         # bs_x = observation["bs_x"]
#         # bs_y = observation["bs_y"]
#         to_bs_x = observation["to_bs_x"]
#         to_bs_y = observation["to_bs_y"]
#         pre_to_bs_x = observation["pre_to_bs_x"]
#         pre_to_bs_y = observation["pre_to_bs_y"]

#         to_bs_dis = observation["to_bs_dis"]
#         pre_to_bs_dis = observation["pre_to_bs_dis"]

#         if score_var != 0: reward += 1500
#         if is_hit: reward += 2000
        
#         get_power = False

#         # if power == 0:
#         if power_var > 0: 
#             get_power = True
#             reward += 3000

#         if to_bs_dis < pre_to_bs_dis:
#             reward += (pre_to_bs_dis - to_bs_dis) * 10
#         elif to_bs_dis == pre_to_bs_dis:
#             reward -= 8
#         else:
#             reward -= (to_bs_dis - pre_to_bs_dis) * 5

#             # if to_bs_x < pre_to_bs_x:
#             #     reward += 500
#             # else: reward -= 200            
            
#             # if to_bs_y < pre_to_bs_y:
#             #     reward += 500
#             # else: reward -= 200
#         # else:
#         #     if power_var < 0:
#         #         if score_var > 0: reward += 500
#         #         else: reward -= 500

#         #     if abs(my_y - cp_y) < 50:
#         #         reward += 500
#         #     else:
#         #         reward -= 200

#         #     if abs(my_x - cp_x) < 250:
#         #         reward += 500
#         #     else:
#         #         reward -= 200

#         print(f"is_hit ? {is_hit} || get score ? {score_var} || power : {power} || get_power ? {get_power} ||\n to_bs_dis : {to_bs_dis} || pre_to_bs_dis : {pre_to_bs_dis} ||  reward : {reward}\n")
#         return reward
    
# #----------------------------------------------------------------------------------------------------------------------------------


    def calculate_angle(vector1, vector2):
        # 向量內積
        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        # 分別計算向量長度
        magnitude1 = math.sqrt(sum(a**2 for a in vector1))
        magnitude2 = math.sqrt(sum(b**2 for b in vector2))
        
        # 檢查分母是否為零 避免 Undefined Behavior
        if magnitude1 * magnitude2 == 0:
            return 0

        # 計算餘弦相似度
        cosine_similarity = dot_product / (magnitude1 * magnitude2)

        # 確保在正負 1 之間並使用反餘弦函數計算餘弦相似度對應的弧度
        angle_in_radians = math.acos(max(-1, min(1, cosine_similarity)))
        # 將弧度轉換為度數，得到兩向量的夾角
        angle_in_degrees = math.degrees(angle_in_radians)
        
        return angle_in_degrees


    def __get_obs(self, scene_info):      

        # 把 scene_info 讀出來
        my_x = scene_info["x"]
        my_y = scene_info["y"]
        pre_my_x = self.pre_scene_info["x"]
        pre_my_y = self.pre_scene_info["y"]
        bs_x = scene_info["bullet_stations_info"][0]["x"]
        bs_y = scene_info["bullet_stations_info"][0]["y"]

        # 位移向量
        target_direction_vector = [bs_x - pre_my_x,bs_y - pre_my_y]
        displacement_vector = [my_x - pre_my_x, my_y - pre_my_y]

        # 計算夾角
        angle = calculate_angle(target_direction_vector, displacement_vector)

        observation = {"power" : power, "power_var" : power_var,
                        "score_var" : score_var, "is_hit" : is_hit,"angle" : angle}

