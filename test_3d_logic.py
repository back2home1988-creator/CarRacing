from ursina import *
from main import setup_game
import os

def test_3d_game_initialization():
    # Ensure headless mode for testing
    os.environ['DISPLAY'] = ''
    app = setup_game()
    assert app is not None

    # Check if key entities exist in the scene
    entities = [e for e in scene.entities]
    # At least camera, road, player, controller, sky
    assert len(entities) >= 4

    # Verify player properties (now red)
    player = next(e for e in entities if hasattr(e, 'color') and e.color == color.red)
    assert player.model is not None
    assert player.collider is not None

    print("test_3d_game_initialization and player check passed")

if __name__ == "__main__":
    try:
        test_3d_game_initialization()
        print("All 3D logic tests passed!")
    except Exception as e:
        print(f"3D tests failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
    finally:
        pass
