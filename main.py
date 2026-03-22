from ursina import *
import random
import os

# Global app variable
app = None

def setup_game():
    global app
    if app is None:
        if not os.environ.get('DISPLAY'):
            app = Ursina(window_type='none')
        else:
            app = Ursina()

    # Camera setup for realistic 3D racing perspective
    camera.position = (0, 7, -25)
    camera.rotation_x = 10

    # Environment
    try:
        sky = Sky()
    except:
        sky = Entity(model='sphere', scale=500, color=color.azure, double_sided=True)

    # Road with a texture
    road = Entity(model='cube', scale=(10, 0.5, 200), color=color.dark_gray, texture='white_cube', position=(0,0,50))

    # Player Car with a more realistic color and texture
    player = Entity(model='cube', color=color.red, scale=(2, 0.8, 4.5), position=(0, 0.4, -10), collider='box', texture='brick')

    obstacles = []

    try:
        score_text = Text(text='Score: 0', position=(-0.85, 0.45), scale=2, color=color.white)
        game_over_text = Text(text='GAME OVER\nPress R to Restart', position=(0, 0.1), origin=(0,0), scale=3, color=color.red, enabled=False)
    except:
        score_text = None
        game_over_text = None

    state = {
        'score': 0,
        'game_over': False,
        'player': player,
        'obstacles': obstacles,
        'score_text': score_text,
        'game_over_text': game_over_text,
        'road': road,
        'spawn_task': None
    }

    def spawn_obstacle():
        # Only spawn if not game over
        if not state['game_over']:
            # Use random models or textures for variety
            obs = Entity(model='cube', color=color.random_color(), scale=(2, 1, 4), position=(random.uniform(-4, 4), 0.5, 100), collider='box', texture='white_cube')
            state['obstacles'].append(obs)
            # Re-invoke to continue spawning
            state['spawn_task'] = invoke(spawn_obstacle, delay=random.uniform(1, 2.5))

    def update():
        if state['game_over']:
            if held_keys['r']:
                restart_game()
            return

        # Simulate movement by scrolling road texture
        speed_val = 1.0 + (state['score'] / 50.0) # Gradually increase speed
        state['road'].texture_offset += (0, speed_val * time.dt)

        # Player movement
        move_speed = 10
        if held_keys['a'] or held_keys['left arrow']:
            state['player'].x -= move_speed * time.dt
        if held_keys['d'] or held_keys['right arrow']:
            state['player'].x += move_speed * time.dt

        # Boundary
        if state['player'].x < -4: state['player'].x = -4
        if state['player'].x > 4: state['player'].x = 4

        # Move obstacles towards player
        for obs in state['obstacles'][:]:
            obs.z -= (50 + state['score']) * time.dt # Speed up with score

            # Collision detection
            if state['player'].intersects(obs).hit:
                state['game_over'] = True
                if state['game_over_text']:
                    state['game_over_text'].enabled = True

            # Score and remove obstacles
            if obs.z < -20:
                state['score'] += 1
                if state['score_text']:
                    state['score_text'].text = f'Score: {state["score"]}'
                state['obstacles'].remove(obs)
                destroy(obs)

    def restart_game():
        state['score'] = 0
        if state['score_text']:
            state['score_text'].text = 'Score: 0'
        state['game_over'] = False
        if state['game_over_text']:
            state['game_over_text'].enabled = False
        state['player'].x = 0
        for obs in state['obstacles']:
            destroy(obs)
        state['obstacles'].clear()

        # Cancel any pending spawn and start fresh
        if state['spawn_task']:
            try:
                state['spawn_task'].enabled = False
            except:
                pass
        spawn_obstacle()

    # Start first spawn
    spawn_obstacle()

    controller = Entity()
    controller.update = update

    return app

if __name__ == "__main__":
    app = setup_game()
    app.run()
