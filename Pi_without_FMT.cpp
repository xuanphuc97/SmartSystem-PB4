#include <bits/stdc++.h>
using namespace std;
#define ND 1000010
#define L10V 5
double X, P10, D10;
int M, N2, L10;
int IV[ND + 1], IXD[ND + 1];
int INO[5] = {2, 3, 3, 4, 4};

int IDATA[5][4][2] = {16, 5, -4, 239, 0, 0, 0, 0,
                      48, 18, 32, 57, -20, 239, 0, 0, 
                      32, 10, -4, 239, -16, 515, 0, 0,
                      176, 57, 28, 239, -48, 682, 96, 12943, 
                      48, 49, 128, 57, -20, 239, 48, 110443};

void ATANV()
{
  int i, k, KOSU, LST, ISG;
  double X2, DX2, W, W1, W2, VK, DK, WK, WK1, WK2;

  X2 = X * X;
  DX2 = 1.0 / X2;
  KOSU = N2 * L10 / (log(X2) / log(10.0));

  for (i = 2; i <= N2; i++)
  {
    IXD[i] = 0;
  }
  IXD[1] = M;

  W2 = 0.0;
  for (i = 1; i <= N2; i++)
  {
    W = IXD[i] + W2 * P10;
    W1 = floor(W / X);
    W2 = W - W1 * X;
    IXD[i] = W1;
    IV[i] = IV[i] + IXD[i];
  }

  LST = 1;
  ISG = -1;
  for (k = 1; k <= KOSU; k++)
  {
    W2 = 0.0;
    WK2 = 0.0;
    VK = 2 * k + 1;
    DK = 1.0 / VK;
    for (i = LST; i <= N2; i++)
    {
      W = IXD[i] + W2 * P10;
      W1 = floor(W * DX2);
      W2 = W - W1 * X2;
      IXD[i] = W1;
      WK = W1 + WK2 * P10;
      WK1 = floor(WK * DK);
      WK2 = WK - WK1 * VK;
      IV[i] = IV[i] + ISG * WK1;
    }
    if (IXD[LST] == 0)
    {
      LST = LST + 1;
      if (IXD[LST] == 0)
        LST = LST + 1;
    }
    ISG = -ISG;
  }
}

void NORMAL()
{
  int i;
  double W, W1;

  for (i = N2; i >= 2; i--)
  {
    W = IV[i];
    W1 = floor(W * D10);
    IV[i - 1] = IV[i - 1] + W1;
    IV[i] = W - W1 * P10;
  }

  {
    if (IV[i] >= P10)
    {
      IV[i] = IV[i] - P10;
      IV[i - 1] = IV[i - 1] + 1;
    }
    if (IV[i] < 0)
    {
      IV[i] = IV[i] + P10;
      IV[i - 1] = IV[i - 1] - 1;
    }
  }
}

int main()
{
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);
  int i, k, ID, NN, N, IX, KETA, T1, T2, T3, T4, KEND;
  double TT3, TT4;

  L10 = L10V;
  P10 = pow(10.0, L10);
  D10 = 1.0 / P10;

  if (ID <= 0 || ID >= 6)
    ID = 1;
  //printf(" Nhap N (N = So chu so thap phan): ") ;
  scanf("%d", &NN);
  N = NN / L10;
  if (N >= ND - 3)
	N = ND - 3;
  NN = N * L10;
  N2 = N + 3;

  for (i = 1; i <= N2; i++)
    IV[i] = 0;

  for (k = 0; k < INO[ID]; k++)
  {
    M = IDATA[ID][k][0];
    X = IDATA[ID][k][1];
    ATANV();
  }

  NORMAL();
  printf(" Pi = 3.");
  for (k = 2; k <= N2 - 2; k = k + 16)
  {
    KEND = k + 15;
    if (KEND > N2 - 2)
      KEND = N2 - 2;
    KETA = (k - 2) * L10 + 1;
    printf("\n");
    for (i = k; i <= KEND; i = i + 2)
    {
      printf(" %5.5d%5.5d", IV[i], IV[i + 1]);
    }
  }
}
