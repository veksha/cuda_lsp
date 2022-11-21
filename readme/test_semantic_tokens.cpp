#define MACR false
const float PI = 3.14;
enum OBJ_TYPE // Object Class Types
{
   OBJ_ITEM,
   OBJ_PLAYER,
};
namespace example { class some {}; }
namespace Game {  
  class Player {
     int property; 
     Player();
     void func1(int param1);
     void func2(const int param2);
  };
  
  Player::Player() {
      int integer;
      integer = 0;
      OBJ_TYPE t = OBJ_TYPE::OBJ_PLAYER;
      char str[] = "string"; 
  }
  void Player::func1(int param1) {
     example::some op1;
     if (MACR)
      param1 = 0;
  }
  void Player::func2(const int param2) {
      const int abc = 0;
      if (param2 == 0) return;  
  }
}
