import gym
from PPO_continuous import PPO, Memory
from PIL import Image
import torch
import pybullet
import pybulletgym.envs

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device = "cpu"

def test():
    ############## Hyperparameters ##############
    env_name = "Walker2DPyBulletEnv-v0"
    env = gym.make(env_name)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]

    n_episodes = 3          # num of episodes to run
    max_timesteps = 1500    # max timesteps in one episode
    render = True           # render the environment
    save_gif = False        # png images are saved in gif folder

    # filename and directory to load model from
    filename = "PPO_continuous_" +env_name+ ".pth"
    directory = "./preTrained/"

    action_std = 0.5        # constant std for action distribution (Multivariate Normal)
    K_epochs = 80           # update policy for K epochs
    eps_clip = 0.2          # clip parameter for PPO
    gamma = 0.99            # discount factor

    lr = 0.0003             # parameters for Adam optimizer
    betas = (0.9, 0.999)
    #############################################

    memory = Memory()
    ppo = PPO(state_dim, action_dim, action_std, lr, betas, gamma, K_epochs, eps_clip)
    # ppo.policy_old.load_state_dict(torch.load(directory+filename, map_location=torch.device('cpu')))

    for ep in range(1, n_episodes+1):
        ep_reward = 0
        state = env.reset()
        for t in range(max_timesteps):
            action = ppo.select_action(state, memory)
            state, reward, done, _ = env.step(action)
            ep_reward += reward
            if render:
                env.render()
            if save_gif:
                 img = env.render(mode = 'rgb_array')
                 img = Image.fromarray(img)
                 img.save('./gif/{}.jpg'.format(t))
            if done:
                break

        print('Episode: {}\tReward: {}'.format(ep, int(ep_reward)))
        ep_reward = 0
        env.close()

if __name__ == '__main__':
    test()

