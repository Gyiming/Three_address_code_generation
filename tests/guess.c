int main(void) {
  int guess;
  int x;
  
  guess = rand();

  do {
	printf("Enter number: ");
	scanf("%d", &x);

	if (x < guess) {
	  printf("guess higher!\n");
	} else if (x > guess) {
	  printf("guess lower!\n");
	} else {
	  printf("correct guess!\n");
	}
  } while(x != guess);
}
