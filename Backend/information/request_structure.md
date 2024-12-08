# Structure of Request dictionary

| #     | field | value type                | meaning                                                      |
| :---: | ---   | ---                       | ---                                                          |
| 1     | id    | int (>= 0)                | id of function to use                                        |
| 2     | track | list[int], which int > 0  | list that represent [one] track                              |
| 3     | args  | list[**Values**]          | represent values that was inputted (in order of declaration) |

*example*:
```json
{
    "id":    1,      // function of id = 1
    "track": [1, 2]  // 2-nd copy of 1-st track, track = 1.2
    "args": [
        12.0         // first [and only] field contain value 12.0
    ]
}
```


# Values
Values is one of the next types (each type corresponds to some type of input in function declaration)

1. Integer
2. Positive integer - integer that is bigger than zero (> 0)
3. Float
4. Positive float - float that is bigger than zero (> 0.0)
5. Non negative float - float that is bigger than or equals to zero (>= 0.0)
6. Time - is dict of {minutes: a, seconds: b}, a is [0, MAX_FLOAT], b is [0, 60] <br/>
    *example*
    ```ts
    a: Time = {minutes: 12, seconds: 1}; // 12:01
    ```
7. Track - input as list of positive integers <br/>
    *example* <br/>
    ```ts
    a: Track = [2];     // track 2
    b: Track = [2, 3];  // 3-rd copy of track 2
    ```
8. Track characteristics - str, one of three values ["frequency", "amplitude", "time"]


# Pipeline-request
Pipeline-request is a list of **Request dictionary**-s.
Pipeline-request is a structure that is been awaited alongside with audio file to make requested pipeline.