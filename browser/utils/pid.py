class PositionalPID:
    """PositionalPID """

    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.SystemOutput = 0.0
        self.ResultValueBack = 0.0
        self.PidOutput = 0.0
        self.PIDErrADD = 0.0
        self.ErrBack = 0.0

    def SetInertiaTime(self, InertiaTime, SampleTime):
        self.SystemOutput = (InertiaTime * self.ResultValueBack + SampleTime * self.PidOutput) / (
                SampleTime + InertiaTime)
        self.ResultValueBack = self.SystemOutput

    def SetStepSignal(self, StepSignal):
        Err = StepSignal - self.SystemOutput
        KpWork = self.Kp * Err
        KiWork = self.Ki * self.PIDErrADD
        KdWork = self.Kd * (Err - self.ErrBack)
        self.PidOutput = KpWork + KiWork + KdWork
        # print(Err)
        self.PIDErrADD += Err
        self.ErrBack = Err


# 测试PID程序
def TestPID(P, I, D, li):
    PositionalPid = PositionalPID(P, I, D)
    PositionalXaxis = [0]
    PositionalYaxis = [0]

    for i in range(1, 100):
        # 位置式
        PositionalPid.SetStepSignal(li)
        PositionalPid.SetInertiaTime(3, 0.1)
        PositionalYaxis.append(PositionalPid.SystemOutput)
        PositionalXaxis.append(i)
    l = []
    for i in range(len(PositionalYaxis) - 1):
        l.append(round(PositionalYaxis[i + 1] - PositionalYaxis[i]))
    return l


def get_pid_track(distance):
    '''
    Here, the PID proportional integral differential adjustment commonly used in industry is used to return the step size of each movement; simulating human round-trip operation
    '''
    lis = TestPID(4.5, 0.5, 0.1, distance)
    return lis


if __name__ == '__main__':
    print(get_pid_track(149))
