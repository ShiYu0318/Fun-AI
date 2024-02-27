import math
from collections import OrderedDict

class Environment():
    def __init__(self) -> None:                                                                        
        self.action_mapping = [["UP"], ["DOWN"], ["LEFT"], ["RIGHT"],["NONE"]]
        self.n_actions = len(self.action_mapping)
        
        self.action = 0 
        self.observation = OrderedDict([('food_direction', 0), ('garbage_direction', 0)])
        self.pre_reward = 0
    
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
        
        reward = self.__get_reward(action, observation)
                
        done = self.scene_info["status"] != "GAME_ALIVE"            

        info = {}

        return observation, reward, done, info
    
#-------------------------------------------------------------------------------------------------------------------------------------

    def __get_obs(self, scene_info):                                             

        FOOD_TYPES = ["FOOD_1", "FOOD_2", "FOOD_3"]
        GARBAGE_TYPES = ["GARBAGE_1", "GARBAGE_2", "GARBAGE_3"]


        # 以食物垃圾的 type 來分類，方便給不同權重的 reward，讓魷魚在做不同選擇時給的 reward 不同

        squid_pos = [scene_info["squid_x"], scene_info["squid_y"]]
        all_food_1_pos = [[food["x"], food["y"]] for food in scene_info["foods"] if food["type"] == "FOOD_1"]
        all_food_2_pos = [[food["x"], food["y"]] for food in scene_info["foods"] if food["type"] == "FOOD_2"]
        all_food_3_pos = [[food["x"], food["y"]] for food in scene_info["foods"] if food["type"] == "FOOD_3"]

        all_garbage_1_pos = [[food["x"], food["y"]] for food in scene_info["foods"] if food["type"] == "GARBAGE_1"]
        all_garbage_2_pos = [[food["x"], food["y"]] for food in scene_info["foods"] if food["type"] == "GARBAGE_2"]
        all_garbage_3_pos = [[food["x"], food["y"]] for food in scene_info["foods"] if food["type"] == "GARBAGE_3"]

        food_1_direction = self.__get_direction_to_nearest(squid_pos, all_food_1_pos) if all_food_1_pos else 0
        food_2_direction = self.__get_direction_to_nearest(squid_pos, all_food_2_pos) if all_food_2_pos else 0
        food_3_direction = self.__get_direction_to_nearest(squid_pos, all_food_3_pos) if all_food_3_pos else 0

        garbage_1_direction = self.__get_direction_to_nearest(squid_pos, all_garbage_1_pos) if all_garbage_1_pos else 0
        garbage_2_direction = self.__get_direction_to_nearest(squid_pos, all_garbage_2_pos) if all_garbage_2_pos else 0
        garbage_3_direction = self.__get_direction_to_nearest(squid_pos, all_garbage_3_pos) if all_garbage_3_pos else 0

        # Return an ordered dictionary containing the computed directions        
        return OrderedDict([('food_1_direction', food_1_direction), 
                            ('food_2_direction', food_2_direction),  
                            ('food_3_direction', food_3_direction), 
                            ('garbage_1_direction', garbage_1_direction), 
                            ('garbage_2_direction', garbage_2_direction), 
                            ('garbage_3_direction', garbage_3_direction)])



    def __get_reward(self, action: int , observation: int):

        reward = self.scene_info["score"] - self.pre_reward
        food_1_direction = observation['food_1_direction']
        food_2_direction = observation['food_2_direction']
        food_3_direction = observation['food_3_direction']
        garbage_1_direction = observation['garbage_1_direction']
        garbage_2_direction = observation['garbage_2_direction']
        garbage_3_direction = observation['garbage_3_direction']

        """
        direction
        action:
        - 0 : up
        - 1 : down
        - 2 : left
        - 3 : right
        - 4 ; none

        - 0: No item is close or items list is empty.
        - 1: right
        - 2: above
        - 3: left
        - 4: below
        """

        food_3_reward = 200
        food_2_reward = 150
        food_1_reward = 100
        food_loss = -50
        
        # 用 greedy 的觀念 給不同的食物不同權重 會優先跑去吃分數高的食物
        if action == 0:
                reward += food_3_reward if food_3_direction == 2 else food_loss
                reward += food_2_reward if food_2_direction == 2 else food_loss
                reward += food_1_reward if food_1_direction == 2 else food_loss
        elif action == 1:
                reward += food_3_reward if food_3_direction == 4 else food_loss
                reward += food_2_reward if food_2_direction == 4 else food_loss
                reward += food_1_reward if food_1_direction == 4 else food_loss
        elif action == 2:
                reward += food_3_reward if food_3_direction == 3 else food_loss
                reward += food_2_reward if food_2_direction == 3 else food_loss
                reward += food_1_reward if food_1_direction == 3 else food_loss
        elif action == 3:
                reward += food_3_reward if food_3_direction == 1 else food_loss
                reward += food_2_reward if food_2_direction == 1 else food_loss
                reward += food_1_reward if food_1_direction == 1 else food_loss
        elif action == 4:
                reward += food_loss


        garbage_3_reward = 500
        garbage_2_reward = 300
        garbage_1_reward = 50
        garbage3_loss = -30
        garbage2_loss = -10
        garbage_loss = -5

        # 第六關以後因為有個難度提升 有較多垃圾 不能像前五關一樣只專注在吃食物 要盡量避免垃圾 且也有不同 reward 優先避開扣分較重的垃圾
        if self.scene_info["score_to_pass"] >= 60:
            if action == 0:
                reward -= garbage_3_reward if garbage_3_direction == 2 else garbage3_loss
                reward -= garbage_2_reward if garbage_2_direction == 2 else garbage2_loss
                reward -= garbage_1_reward if garbage_1_direction == 2 else garbage_loss

            elif action == 1:
                reward -= garbage_3_reward if garbage_3_direction == 4 else garbage3_loss
                reward -= garbage_2_reward if garbage_2_direction == 4 else garbage2_loss
                reward -= garbage_1_reward if garbage_1_direction == 4 else garbage_loss
            elif action == 2:
                reward -= garbage_3_reward if garbage_3_direction == 3 else garbage3_loss
                reward -= garbage_2_reward if garbage_2_direction == 3 else garbage2_loss
                reward -= garbage_1_reward if garbage_1_direction == 3 else garbage_loss
            elif action == 3:
                reward -= garbage_3_reward if garbage_3_direction == 1 else garbage3_loss
                reward -= garbage_2_reward if garbage_2_direction == 1 else garbage2_loss
                reward -= garbage_1_reward if garbage_1_direction == 1 else garbage_loss
            elif action == 4:
                reward += garbage2_loss

        print(action,reward)
        self.pre_reward = self.scene_info["score"] 
        return reward

        # 可再改良 距離判斷 若食物方向和垃圾方向一樣 請先避開垃圾
        # 可再改良 冷靜機制 當分數快接近目標時 將避開垃圾的權重提高 可以不用急著吃食物

#-------------------------------------------------------------------------------------------------------------------------------------

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
    
    def __find_closest_point(self, points:list, target_point:list):
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
            distance = self.__calculate_distance(point, target_point)
            if distance < min_distance:
                min_distance = distance
                closest_point = point

        return closest_point
    
    def __determine_relative_position(self, reference_point: list, target_point: list) -> int:
        """
        Determines the relative position of the target point in relation to the reference point.

        Parameters:
        reference_point (list): The reference point as a list of coordinates [x, y].
        target_point (list): The target point as a list of coordinates [x, y].

        Returns:
        int: The relative position of the target point with respect to the reference point.
            - 0: No food or garbage.
            - 1: Food or garbage is to the right of the squid.
            - 2: Food or garbage is above the squid.
            - 3: Food or garbage is to the left of the squid.
            - 4: Food or garbage is below the squid.
        """
        # Calculate relative coordinates
        delta_x = target_point[0] - reference_point[0]
        delta_y = target_point[1] - reference_point[1]

        # Determine the region based on the sum and difference of the relative coordinates
        if delta_x + delta_y > 0:
            if delta_x - delta_y > 0:
                return 1  # Right
            else:
                return 4  # Up
        else:
            if delta_x - delta_y > 0:
                return 2  # Down
            else:
                return 3  # Left
    
    def __get_direction_to_nearest(self, squid_pos: list, items_pos: list) -> int:
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
        closest_item_pos = self.__find_closest_point(items_pos, squid_pos)
        if closest_item_pos is not None:
            return self.__determine_relative_position(squid_pos, closest_item_pos)
        return 0  # Return 0 if no closest item is found