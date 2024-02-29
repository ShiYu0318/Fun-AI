import math
from collections import OrderedDict

class Environment():
    def __init__(self) -> None:                                                                        
        self.action_mapping = [['FORWARD'],['BACKWARD'],['TURN_LEFT'],['TURN_RIGHT'],['AIM_LEFT'],['AIM_RIGHT'],['SHOOT']]
        # self.action_mapping = [['NONE'],['NONE'],['NONE'],['NONE'],['NONE'],['NONE'],['NONE']]
        #self.action_mapping = [['FORWARD'],['BACKWARD'],['TURN_LEFT'],['TURN_RIGHT'],['AIM_LEFT'],['AIM_RIGHT'],['SHOOT']]
        self.n_actions = len(self.action_mapping)
        self.angle=0
        self.angle_number=0
        self.self_angle=0
        self.self_angle_number=0
        self.self_gun_angle_number=0
        self.oil=0
        self.action = 0 
        self.observation = 0
        self.pre_reward = 0
        self.prrbullets=0
        self.prbullets=0
        self.reframe=0 #scene_info["used_frame"]
        self.pre_scene_info = {"x":0, "y":0}
        self.delta_x=0
        self.delta_y=0

        self.prroil=0
        self.proil=0

        self.frame=0
        
    def set_scene_info(self, Scene_info: dict):
        """
        Stores the given scene information into the environment.

        Parameters:
        scene_info (dict): A dictionary containing environment information.
        """
        self.scene_info = Scene_info        
    
    def reset(self):
        """
        Resets the environment and returns the initial observation.

        Returns:
        observation: The initial state of the environment after reset.
        """
        observation = self.__get_obs(self.scene_info)

        return observation
    
    def step(self, action: int):   
        """
        Executes a given action in the environment and returns the resulting state.

        Parameters:
        action (int): The action to be performed, representing the squid's movement.

        Returns:
        observation: The current state of the environment after the action.
        reward (int): The reward obtained as a result of performing the action.
        done (bool): Indicates whether the game has ended (True if ended, False otherwise).
        info (dict): Additional information about the current state.
        """
        reward = 0
        observation = self.__get_obs(self.scene_info)                  
        
        reward = self.__get_reward(observation,action)
                
        done = self.scene_info["status"] != "GAME_ALIVE"            

        info = {}

        return observation, reward, done, info
    
    ##########  to do  ##########
    def __get_obs(self, scene_info):  
        observation = {}    



        wall_TYPES = ['wall_4','wall_3','wall_2','wall_1']
        ##--- scene_info['walls_info']

        #bullets_TYPES = ['bullets']#彈藥
        ## --  scene_info['bullet_stations_info']
        
            
        ##-- scene_info['oil_stations_info']

        
        tank_pos = [scene_info["x"], scene_info["y"]]

        #油-------


        self.prrbullets=self.prbullets
        self.prbullets=scene_info['power']
        if(scene_info['power']-self.prrbullets>1):
            self.frame=scene_info["used_frame"]


        self.prroil=self.proil
        self.proil=scene_info['oil']
        if(scene_info['oil']-self.prroil>1):
            self.frame=scene_info["used_frame"]

            

        # print(scene_info["used_frame"]-self.frame)
        oil_TYPES = ['bullets']#子彈
        oil_info=scene_info['bullet_stations_info']
        if(scene_info["id"]=='1P'):
            del oil_info[1]
        if(scene_info["id"]=='2P'):
            del oil_info[0]


        if(scene_info["used_frame"]-self.frame>=200 or scene_info['oil']<20):
            #------------------------------------------
            oil_TYPES = ['oil']#油箱
            oil_info=scene_info['oil_stations_info']
            if(scene_info["id"]=='1P'):
                del oil_info[0]
            if(scene_info["id"]=='2P'):
                del oil_info[1]
       
            




        all_oil_pos = [[enemy["x"], enemy["y"]] for enemy in oil_info if enemy["id"] in oil_TYPES]
        #油-------

        #一般
        

        

        dis = math.sqrt((scene_info['competitor_info'][0]['x'] - scene_info["x"])**2 + (scene_info['competitor_info'][0]['y'] - scene_info["y"])**2)
        all_enemy_pos = [[enemy["x"], enemy["y"]] for enemy in scene_info['walls_info'] if enemy["id"] in wall_TYPES]



        







#-----------------------------------------------第一組
    
        if(scene_info["id"]=='1P'):
            all_enemy_pos_x_y=[500, 300]
        if(scene_info["id"]=='2P'):
            all_enemy_pos_x_y=[450, 250]
        try:
            # 使用index()方法查找元素索引
            if all_enemy_pos.index(all_enemy_pos_x_y) >0:
                all_enemy_pos=[all_enemy_pos_x_y]
        except ValueError:
            None     
              
#-------------------------------------------------------
        # if(scene_info["id"]=='1P'):
        #     all_enemy_pos_x_y=[500, 400]
        # if(scene_info["id"]=='2P'):
        #     all_enemy_pos_x_y=[300, 250]
        # try:
        #     # 使用index()方法查找元素索引
        #     if all_enemy_pos.index(all_enemy_pos_x_y) >0:
        #         all_enemy_pos=[all_enemy_pos_x_y]
        # except ValueError:
        #     None

        # if(scene_info["id"]=='2P'):
        #     all_enemy_pos_x_y=[500, 400]
        # if(scene_info["id"]=='1P'):
        #     all_enemy_pos_x_y=[300, 250]
        # try:
        #     # 使用index()方法查找元素索引
        #     if all_enemy_pos.index(all_enemy_pos_x_y) >0:
        #         all_enemy_pos=[all_enemy_pos_x_y]
        # except ValueError:
        #     None

#-------------------------------------------------------
        # if(scene_info["id"]=='1P'):
        #     all_enemy_pos_x_y=[500, 500]
        # if(scene_info["id"]=='2P'):
        #     all_enemy_pos_x_y=[200, 250]
        # try:
        #     # 使用index()方法查找元素索引
        #     if all_enemy_pos.index(all_enemy_pos_x_y) >0:
        #         all_enemy_pos=[all_enemy_pos_x_y]
        # except ValueError:
        #     None

        # if(scene_info["id"]=='2P'):
        #     all_enemy_pos_x_y=[500, 500]
        # if(scene_info["id"]=='1P'):
        #     all_enemy_pos_x_y=[200, 250]
        # try:
        #     # 使用index()方法查找元素索引
        #     if all_enemy_pos.index(all_enemy_pos_x_y) >0:
        #         all_enemy_pos=[all_enemy_pos_x_y]
        # except ValueError:
        #     None
#-------------------------------------------------------
        # if(scene_info["id"]=='1P'):
        #     all_enemy_pos_x_y=[500, 600]
        # if(scene_info["id"]=='2P'):
        #     all_enemy_pos_x_y=[100, 250]
        # try:
        #     # 使用index()方法查找元素索引
        #     if all_enemy_pos.index(all_enemy_pos_x_y) >0:
        #         all_enemy_pos=[all_enemy_pos_x_y]
        # except ValueError:
        #     None

        # if(scene_info["id"]=='2P'):
        #     all_enemy_pos_x_y=[500, 600]
        # if(scene_info["id"]=='1P'):
        #     all_enemy_pos_x_y=[100, 250]
        # try:
        #     # 使用index()方法查找元素索引
        #     if all_enemy_pos.index(all_enemy_pos_x_y) >0:
        #         all_enemy_pos=[all_enemy_pos_x_y]
        # except ValueError:
        #     None

#-------------------------------------------------------
        #320
        if dis<=400:#400#1
            all_enemy_pos = [[scene_info['competitor_info'][0]['x'],scene_info['competitor_info'][0]['y']]]
        
        # print(scene_info['walls_info'])
        # print()
        # print()



        oil_direction = self.__get_direction_to_nearest(tank_pos, all_oil_pos) if all_oil_pos else 0
        enemy_direction = self.__get_direction_to_nearest(tank_pos, all_enemy_pos) if all_enemy_pos else 0

        

        self.oil=oil_direction
        self.enemy=enemy_direction


        

        if scene_info["angle"]==0:
            self.self_angle_number=5
        if scene_info["angle"]==45:
            self.self_angle_number=6
        if scene_info["angle"]==90:
            self.self_angle_number=7
        if scene_info["angle"]==135:
            self.self_angle_number=8
        if scene_info["angle"]==180:
            self.self_angle_number=1
        if scene_info["angle"]==225:
            self.self_angle_number=2
        if scene_info["angle"]==270:
            self.self_angle_number=3
        if scene_info["angle"]==315:
            self.self_angle_number=4
        if scene_info["angle"]==360:
            self.self_angle_number=5
        self.self_angle=scene_info["angle"]


        if scene_info['gun_angle']==0:
            self.self_gun_angle_number=5
        if scene_info['gun_angle']==45:
            self.self_gun_angle_number=6
        if scene_info['gun_angle']==90:
            self.self_gun_angle_number=7
        if scene_info['gun_angle']==135:
            self.self_gun_angle_number=8
        if scene_info['gun_angle']==180:
            self.self_gun_angle_number=1
        if scene_info['gun_angle']==225:
            self.self_gun_angle_number=2
        if scene_info['gun_angle']==270:
            self.self_gun_angle_number=3
        if scene_info['gun_angle']==315:
            self.self_gun_angle_number=4
        if scene_info['gun_angle']==360:
            self.self_gun_angle_number=5








        # observation["id"]= scene_info["id"][0]
        observation["oil"]= oil_direction
        observation["enemy"]= enemy_direction

        
        
        observation["face"]= self.self_angle_number
        observation["gun_face"]= self.self_gun_angle_number

        if(scene_info["cooldown"]>0):#0：冷卻好
            observation["cooldow"]=1
        else:
            observation["cooldow"]=0




        
        if(scene_info['power']>0):
            observation["power"]= 1
        else:
            observation["power"]= 0


        # if(self.self_angle_number==self.oil ):
        #     observation["turn_or_Front"]=1
        # else:
        #     observation["turn_or_Front"]=0





        

        #8個方向
        #是否可以擊中目標
            




        #
            
        # #self.delta_x
        # self.delta_x+=50
        # self.delta_y+=50

        # print(self.self_gun_angle_number,enemy_direction,observation["cooldow"],self.delta_x,self.delta_y)
        
        # if  (    enemy_direction==self.self_gun_angle_number  and  enemy_direction==1 and self.delta_y>25 and self.delta_y<-50 ):
        #     observation["cooldow"]=1
        # if  (    enemy_direction==self.self_gun_angle_number  and  enemy_direction==5 and self.delta_y>25 and self.delta_y<-50 ):
        #     observation["cooldow"]=1

        # if  (    enemy_direction==self.self_gun_angle_number  and  enemy_direction==2 and self.delta_x + self.delta_y + 25 >0 and self.delta_x + self.delta_y - 25 <0 ):
        #     observation["cooldow"]=1
        # if  (    enemy_direction==self.self_gun_angle_number  and  enemy_direction==6 and self.delta_x + self.delta_y + 25 >0 and self.delta_x + self.delta_y - 25 <0 ):
        #     observation["cooldow"]=1
            
        # if  (    enemy_direction==self.self_gun_angle_number  and  enemy_direction==3 and self.delta_x>50 and self.delta_x<-50 ):
        #     observation["cooldow"]=1
        # if  (    enemy_direction==self.self_gun_angle_number  and  enemy_direction==7 and self.delta_x>50 and self.delta_x<-50 ):
        #     observation["cooldow"]=1

        # if  (    enemy_direction==self.self_gun_angle_number  and  enemy_direction==4 and self.delta_x - self.delta_y + 25 >0 and self.delta_x - self.delta_y - 25 <0 ):
        #     observation["cooldow"]=1
        # if  (    enemy_direction==self.self_gun_angle_number  and  enemy_direction==8 and self.delta_x - self.delta_y + 25 >0 and self.delta_x - self.delta_y - 25 <0 ):
        #     observation["cooldow"]=1

        if enemy_direction!=self.self_gun_angle_number:
            observation["cooldow"]=1

        # print(self.self_gun_angle_number,enemy_direction,observation["cooldow"],self.delta_x,self.delta_y)
        
        






        



        #{'oil': 3, 'enemy': 1, 'face': 5, 'gun_face': 3, 'cooldow': 0, 'power': 0}
        return observation
        #對手資訊
        #[{'id': '2P', 'x': 100, 'y': 300, 'speed': 8, 'score': 0, 'power': 10, 'oil': 100, 
        #'lives': 3, 'angle': 180, 'gun_angle': 180, 'cooldown': 0}]
        
        
    ##########  to do  ##########
    def __get_reward(self, observation,action):     
        #     0           1             2             3             4             5          6
        #['FORWARD'],['BACKWARD'],['TURN_LEFT'],['TURN_RIGHT'],['AIM_LEFT'],['AIM_RIGHT'],['SHOOT']   
        reward = 0  


        if(self.scene_info["cooldown"]==0 and self.scene_info['power']>0):
                if action == 6:
                    reward+=5
                else:
                    reward-=10     

        
        else:
        #shoot-------------------

            if(self.self_gun_angle_number!=self.enemy and self.scene_info['power']>0):
                if self.self_gun_angle_number==1 and (self.enemy==2 or self.enemy==3 or self.enemy==4 or self.enemy==5):
                    if action == 4:
                        reward+=5
                    else:
                        reward-=10
                if self.self_gun_angle_number==1 and (self.enemy==6 or self.enemy==7 or self.enemy==8):
                    if action == 5:
                        reward+=5
                    else:
                        reward-=10
                #--------------
                if self.self_gun_angle_number==2 and (self.enemy==6 or self.enemy==3 or self.enemy==4 or self.enemy==5):
                    if action == 4:
                        reward+=5
                    else:
                        reward-=10
                if self.self_gun_angle_number==2 and (self.enemy==1 or self.enemy==7 or self.enemy==8):
                    if action == 5:
                        reward+=5
                    else:
                        reward-=10
                #--------------
                if self.self_gun_angle_number==3 and (self.enemy==6 or self.enemy==7 or self.enemy==4 or self.enemy==5):
                    if action == 4:
                        reward+=5
                    else:
                        reward-=10
                if self.self_gun_angle_number==3 and (self.enemy==1 or self.enemy==2 or self.enemy==8):
                    if action == 5:
                        reward+=5
                    else:
                        reward-=10
                #--------------
                if self.self_gun_angle_number==4 and (self.enemy==6 or self.enemy==7 or self.enemy==8 or self.enemy==5):
                    if action == 4:
                        reward+=5
                    else:
                        reward-=10
                if self.self_gun_angle_number==4 and (self.enemy==1 or self.enemy==2 or self.enemy==3):
                    if action == 5:
                        reward+=5
                    else:
                        reward-=10
                #--------------
                if self.self_gun_angle_number==5 and (self.enemy==6 or self.enemy==7 or self.enemy==8 or self.enemy==1):
                    if action == 4:
                        reward+=5
                    else:
                        reward-=10
                if self.self_gun_angle_number==5 and (self.enemy==4 or self.enemy==2 or self.enemy==3):
                    if action == 5:
                        reward+=5
                    else:
                        reward-=10
                #--------------
                if self.self_gun_angle_number==6 and (self.enemy==2 or self.enemy==7 or self.enemy==8 or self.enemy==1):
                    if action == 4:
                        reward+=5
                    else:
                        reward-=10
                if self.self_gun_angle_number==6 and (self.enemy==4 or self.enemy==5 or self.enemy==3):
                    if action == 5:
                        reward+=5
                    else:
                        reward-=10
                #--------------
                if self.self_gun_angle_number==7 and (self.enemy==2 or self.enemy==3 or self.enemy==8 or self.enemy==1):
                    if action == 4:
                        reward+=5
                    else:
                        reward-=10
                if self.self_gun_angle_number==7 and (self.enemy==4 or self.enemy==5 or self.enemy==6):
                    if action == 5:
                        reward+=5
                    else:
                        reward-=10
                #--------------
                if self.self_gun_angle_number==8 and (self.enemy==2 or self.enemy==3 or self.enemy==4 or self.enemy==1):
                    if action == 4:
                        reward+=5
                    else:
                        reward-=10
                if self.self_gun_angle_number==8 and (self.enemy==7 or self.enemy==5 or self.enemy==6):
                    if action == 5:
                        reward+=5
                    else:
                        reward-=10
            
            else:

            #oil---------------------------------
                if(self.self_angle_number==self.oil ):
                    if action == 0:
                        reward+=5
                    else:
                        reward-=10
                else:
                    ##方向不一樣
                    if self.self_angle_number==1 and (self.oil==5):
                        if action == 1:
                            reward+=5
                        else:
                            reward-=10

                            
                    if self.self_angle_number==1 and (self.oil==4):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==1 and (self.oil==6):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10

                    
                    if self.self_angle_number==1 and (self.oil==2 or self.oil==3):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==1 and ( self.oil==7 or self.oil==8):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    #--------------
                    if self.self_angle_number==2 and (self.oil==6):
                        if action == 1:
                            reward+=5
                        else:
                            reward-=10

                    if self.self_angle_number==2 and (self.oil==5):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==2 and (self.oil==7):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10




                    if self.self_angle_number==2 and (self.oil==3 or self.oil==4 ):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==2 and (self.oil==1  or self.oil==8):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    #--------------
                    if self.self_angle_number==3 and (self.oil==7):
                        if action == 1:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==3 and (self.oil==6 ):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==3 and (self.oil==8):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10


                    if self.self_angle_number==3 and ( self.oil==4 or self.oil==5):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==3 and (self.oil==1 or self.oil==2 ):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    #--------------
                    if self.self_angle_number==4 and (self.oil==8):
                        if action == 1:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==4 and (self.oil==1):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==4 and (self.oil==7):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10


                    if self.self_angle_number==4 and (self.oil==6  or self.oil==5):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==4 and ( self.oil==2 or self.oil==3):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    #--------------
                    if self.self_angle_number==5 and (self.oil==1):
                        if action == 1:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==5 and ( self.oil==2):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==5 and (self.oil==8):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10






                    if self.self_angle_number==5 and (self.oil==6 or self.oil==7 ):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==5 and (self.oil==4 or self.oil==3):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    #--------------
                    if self.self_angle_number==6 and (self.oil==2):
                        if action == 1:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==6 and (self.oil==1):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==6 and ( self.oil==3):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==6 and ( self.oil==7 or self.oil==8):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==6 and (self.oil==4 or self.oil==5):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    #--------------
                    if self.self_angle_number==7 and ( self.oil==3):
                        if action == 1:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==7 and (self.oil==2):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==7 and (self.oil==4 ):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==7 and (self.oil==8 or self.oil==1):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==7 and (self.oil==5 or self.oil==6):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    #--------------
                    if self.self_angle_number==8 and (self.oil==4):
                        if action == 1:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==8 and ( self.oil==3):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==8 and ( self.oil==5):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==8 and (self.oil==2 or self.oil==4 or self.oil==1):
                        if action == 2:
                            reward+=5
                        else:
                            reward-=10
                    if self.self_angle_number==8 and (self.oil==7 or self.oil==6):
                        if action == 3:
                            reward+=5
                        else:
                            reward-=10
            #oil------------------------------------------------------------
            #oil------------------------------------------------------------
            #oil------------------------------------------------------------
            #oil------------------------------------------------------------
            #oil------------------------------------------------------------
            #oil------------------------------------------------------------
            #oil------------------------------------------------------------
                    

    
    
            


        return reward
    

    def __get_direction_to_nearest(self, tank_pos: list, enemy_pos: list) -> int:
        """
        Determines the direction of the nearest item from the squid's position.

        Parameters:
        squid_pos (list): The squid's position as a list of coordinates [x, y].
        items_pos (list): A list of positions of items, where each position is a list of coordinates [x, y].

        Returns:
        int: The direction of the closest item relative to the squid's position. The return values are:
            - 0: No item is close or items list is empty.
            - 1: Closest item is to the right of the squid.
            - 2: Closest item is above the squid.
            - 3: Closest item is to the left of the squid.
            - 4: Closest item is below the squid.
        """
        closest_item_pos = self.__find_closest_point(enemy_pos, tank_pos)
        if closest_item_pos is not None:
            return self.__determine_relative_position(tank_pos, closest_item_pos)
        return 0  # Return 0 if no closest item is found
    
    def __find_closest_point(self, points:list, enemy_point:list):
        """
        Finds the point closest to the target point from a given set of points.

        Parameters:
        points (list): A collection of points, each point being a list of coordinates [x, y].
        target_point (list): The target point as a list of coordinates [x, y].

        Returns:
        list: The point from 'points' that is closest to 'target_point'. Returns None if 'points' is empty.
        """
        min_distance = float('inf')
        closest_point = None

        for point in points:
            distance = self.__calculate_distance(point, enemy_point)
            if distance < min_distance:
                min_distance = distance
                closest_point = point

        
        #pei

        self.oil_x=closest_point[0]
        self.oil_y=closest_point[1]

        return closest_point
    
    
    def __determine_relative_position(self, reference_point: list, enemy_point: list) -> int:
        """
        Determines the relative position of the target point in relation to the reference point.

        Parameters:
        reference_point (list): The reference point as a list of coordinates [x, y].
        target_point (list): The target point as a list of coordinates [x, y].

        Returns:
        int: The relative position of the target point with respect to the reference point.
            - 0: No enemy or enemy .
            - 1: enemy or garbage is to the right of the tank.
            - 2: enemy or garbage is above the tank.
            - 3: enemy or garbage is to the left of the tank.
            - 4: enemy or garbage is below the tank.
        """
        # Calculate relative coordinates
        delta_x =enemy_point[0] - reference_point[0]
        delta_y =enemy_point[1] - reference_point[1]
        
        

        # Determine the region based on the sum and difference of the relative coordinates

        if(delta_x==0):
            delta_x=0.001
        angle=math.degrees(math.atan(delta_y/delta_x))




        #敵人角度
        self.angle=angle

        if(delta_x>0 and delta_y*-1==0):
            self.angle=0
        if(delta_x==0 and delta_y*-1>0):
            self.angle=90
        if(delta_x<0 and delta_y*-1==0):
            self.angle=180
        if(delta_x==0 and delta_y*-1<0):
            self.angle=270

        if(delta_x>0 and delta_y*-1>0):
            self.angle=abs(angle)
        if(delta_x<0 and delta_y*-1>0):
            self.angle=90-angle+90
        if(delta_x<0 and delta_y*-1<0):
            self.angle=abs(angle)+180
        if(delta_x>0 and delta_y*-1<0):
            self.angle=90-angle+90+180


        



        


        

        face=0

        if delta_x + delta_y > 0:
            if delta_x - delta_y > 0:
                face= 1  # Right
            else:
                face= 4  # Up
        else:
            if delta_x - delta_y > 0:
                face= 2  # Down
            else:
                face= 3  # Left

        


        self.delta_x=delta_x
        self.delta_y=delta_y

        
        #--------------
        if face==1 and angle<=22.5 and angle>=-22.5:
            return 1
        if face==2 and (angle<=-67.5 or angle>=67.5):
            return 3
        if face==3 and angle<=22.5 and angle>=-22.5:
            return 5
        if face==4 and (angle<=-67.5 or angle>=67.5):
            return 7
        

        



        if( angle>=-67.5 and angle<=-22.5) and  (delta_x>0 and delta_y<0):
            return 2
        if( angle<=67.5 and angle>=22.5) and  (delta_x<0 and delta_y<0):
            return 4
        if( angle>=-67.5 and angle<=-22.5) and  (delta_x<0 and delta_y>0):
            return 6
        if( angle<=67.5 and angle>=22.5) and  (delta_x>0 and delta_y>0):
            return 8
        #--------------

        
            
        
            
    def __calculate_distance(self, point1: list, point2: list)->float:
        """
        Calculates the Euclidean distance between two points.

        Parameters:
        point1 (list): The coordinates [x, y] of the first point.
        point2 (list): The coordinates [x, y] of the second point.

        Returns:
        float: The Euclidean distance between point1 and point2.
        """
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)