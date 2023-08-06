from collections import deque
from .control import MouseControl, KeyControl

class Module:

    def __init__(self, name, detector):
        self.name = name
        self.detector = detector
        self.mapping = {}
        self.actions = deque()
        self.dfs = deque()
        self.max_data_len = 60
        self.max_action_len = 1
        
    def add_mapping(self, control, actions):
        if isinstance(actions, str):
            actions = [actions]

        if len(actions) > self.max_action_len:
            self.max_action_len = len(actions)

        self.mapping[str(actions)] = control

    def add_transition(self, control, actions):
        self.add_mapping(control, actions)

    def add_mouse_mapping(self, control, action, **params):
        self.add_mapping(MouseControl(control, **params), action)

    def add_key_mapping(self, control, action):
        self.add_mapping(KeyControl(control), action)

    # actions to control
    def __call__(self, df):

        action = self.detector(df)
        self.update_actions(action)
        self.update_dfs(df)

        if len(self.actions) < self.max_action_len:
            return False

        for action_len in range(self.max_action_len, 0, -1):
            actions = [self.actions[i] for i in range(len(self.actions)-action_len,
                                 len(self.actions))]
            actions_str = str(actions)
            if actions_str in self.mapping:
                control = self.mapping[actions_str] # control can be a module to transit between modules
                
                if hasattr(control, "method_name") and "move_diff" in control.method_name:
                    if control.method_name == "right_move_diff":
                        fix_points = ["r_w"]
                    if control.method_name == "left_move_diff":
                        fix_points = ["l_w"]

                    fix_points_cols_x = [c + "_x" for c in fix_points]
                    fix_points_cols_y = [c + "_y" for c in fix_points]
                    control.set_params(df_data_1_x = self.dfs[-2][fix_points_cols_x], 
                                       df_data_2_x = self.dfs[-1][fix_points_cols_x],
                                       df_data_1_y = self.dfs[-2][fix_points_cols_y],
                                       df_data_2_y = self.dfs[-1][fix_points_cols_y])

                return control

        return False

    def update_actions(self, action):
        self.actions.append(action)
        if len(action) > self.max_data_len:
            self.actions.pop_left()

    def update_dfs(self, df):
        self.dfs.append(df)
        if len(df) > self.max_data_len:
            self.dfs.pop_left()

    def reset(self):
        self.actions = deque()
        self.dfs = deque()
        