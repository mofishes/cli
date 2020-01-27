#include <mofish.h>

#include "gtest/gtest.h"

TEST(add_test, add) {
  double res;
  res = add(1, 2);
  ASSERT_NEAR(res, 3, 1.0e-11);
}
