stateDiagram-v2
    %% =======================
    %% Commander (EDH) Lifecycle – State Machine
    %% =======================

    [*] --> PreGame

    %% === PRE-GAME ===
    PreGame: "Pre-Game Setup"
    note right of PreGame
      - Reveal commanders to command zone
      - Shuffle, draw 7, London Mulligan
      - Set life = 40
      - Determine starting player
    end note
    PreGame --> BeginningPhase

    %% === TURN STRUCTURE ===
    BeginningPhase: "Beginning Phase"
    BeginningPhase --> Untap: "Untap Step"
    Untap: "Untap Step"
    note right of Untap
      - No priority in this step
    end note
    Untap --> Upkeep

    Upkeep: "Upkeep Step"
    note right of Upkeep
      - Begin-of-upkeep triggers occur
      - Then players receive priority
    end note
    Upkeep --> DrawStep

    DrawStep: "Draw Step"
    note right of DrawStep
      - Active player draws a card
      - Then players receive priority
    end note
    DrawStep --> PrecombatMain

    PrecombatMain: "Precombat Main Phase"
    note right of PrecombatMain
      - Sorcery-speed actions allowed
      - Lands may be played if legal
    end note
    PrecombatMain --> CombatPhase

    CombatPhase: "Combat Phase"
    CombatPhase --> BeginCombat: "Beginning of Combat"
    BeginCombat: "Beginning of Combat Step"
    note right of BeginCombat
      - Players receive priority
    end note
    BeginCombat --> Attackers

    Attackers: "Declare Attackers Step"
    note right of Attackers
      - Declare attackers
      - Then players receive priority
    end note
    Attackers --> Blockers

    Blockers: "Declare Blockers Step"
    note right of Blockers
      - Declare blockers
      - Then players receive priority
    end note
    Blockers --> CombatDamage

    CombatDamage: "Combat Damage Step"
    note right of CombatDamage
      - Assign and deal combat damage
      - Then players receive priority
    end note
    CombatDamage --> EndCombat

    EndCombat: "End of Combat Step"
    note right of EndCombat
      - Players receive priority
    end note
    EndCombat --> PostcombatMain

    PostcombatMain: "Postcombat Main Phase"
    note right of PostcombatMain
      - Sorcery-speed actions allowed
      - Lands may be played if legal
    end note
    PostcombatMain --> EndingPhase

    EndingPhase: "Ending Phase"
    EndingPhase --> EndStep

    EndStep: "End Step"
    note right of EndStep
      - "At the beginning of the end step" triggers occur
      - Players receive priority
    end note
    EndStep --> Cleanup

    Cleanup: "Cleanup Step"
    note right of Cleanup
      - Discard to maximum hand size
      - Remove damage from permanents
      - End "until end of turn" effects
      - No priority unless a trigger occurs
      - If a trigger occurs, perform another cleanup step
    end note

    %% Terminal return after full cleanup
    Cleanup --> [*]

    %% === PRIORITY / APNAP BLOCK ===
    state PriorityCycle
        [*] --> SBAs
        SBAs --> APNAP
        APNAP --> QueueTriggers
        QueueTriggers --> GrantPrio
        GrantPrio --> PlayerAction
        PlayerAction --> SBAs: "If an action resolved or changed state"
        GrantPrio --> Pass: "All players pass and stack empty"
        Pass --> NextStep

        SBAs: "State-Based Actions"
        note right of SBAs
          - Loop until no SBAs apply
          - Life 0 or less
          - Attempts to draw from empty library
          - 10+ poison counters (2HG 15)
          - 21+ commander combat damage from one commander
          - Lethal damage destroys creatures
          - Tokens leaving battlefield cease to exist
          - +1/+1 and -1/-1 counters cancel in pairs
        end note

        APNAP: "APNAP Ordering"
        note right of APNAP
          - Active player first
          - Then nonactive players in turn order
          - Used for stacking triggers and simultaneous choices
        end note

        QueueTriggers: "Queue Triggers"
        note right of QueueTriggers
          - Put triggered abilities on the stack in APNAP order
        end note

        GrantPrio: "Grant Priority"
        note right of GrantPrio
          - Active player first, then clockwise
        end note

        PlayerAction: "Player Action"
        note right of PlayerAction
          - Cast instant spells, activate abilities, or take special actions when you have priority
          - Noninstant spells only during a main phase with an empty stack and you have priority
          - Mana abilities may be used when paying costs or when you have priority and do not use the stack
        end note

        Pass: "Pass Priority"
        NextStep: "Advance Step/Phase"
    end

    %% Hook the priority cycle to each step that gives priority
    Upkeep --> PriorityCycle
    DrawStep --> PriorityCycle
    PrecombatMain --> PriorityCycle
    BeginCombat --> PriorityCycle
    Attackers --> PriorityCycle
    Blockers --> PriorityCycle
    CombatDamage --> PriorityCycle
    EndCombat --> PriorityCycle
    PostcombatMain --> PriorityCycle
    EndStep --> PriorityCycle

    %% === ZONE CHANGES ===
    ZoneChange: "Zone Change"
    note right of ZoneChange
      - Object becomes a new object on zone change (with rule-defined exceptions)
      - Public zones: battlefield, stack, graveyards, exile, command
      - Hidden zones: hands, libraries
      - Commander: if it would go to graveyard/exile, owner may move it to command zone
      - Commander: if it would go to hand/library, a replacement may move it to command zone
    end note
    PriorityCycle --> ZoneChange
    ZoneChange --> PriorityCycle

    %% === SIMULTANEOUS CHOICES DURING RESOLUTION (APNAP applies) ===
    SimulChoices: "Simultaneous Choices During Resolution"
    note right of SimulChoices
      - When multiple players must make choices simultaneously during resolution, apply APNAP order
    end note
    PriorityCycle --> SimulChoices
    SimulChoices --> APNAP

    %% === OUTCOME EVALUATION ===
    OutcomesCheck: "Outcome Evaluation"
    note right of OutcomesCheck
      - Evaluate terminal results before returning to play
      - Sole survivor wins
      - If a player would win and lose simultaneously, that player loses
    end note

    PriorityCycle --> OutcomesCheck: "Effect says win/lose or a player concedes"
    SBAs_Global: "SBA Loss Sources"
    note right of SBAs_Global
      - Feed SBA-detected losses into outcome evaluation
    end note
    SBAs_Global --> OutcomesCheck
    PriorityCycle --> SBAs_Global: "SBA losses detected"

    OutcomesCheck --> Win: "Any win condition applies"
    OutcomesCheck --> Lose: "Any loss condition applies (not all players at once)"
    OutcomesCheck --> GameDraw: "Simultaneous losses or unbreakable loop"
    OutcomesCheck --> ReturnToPlay: "No terminal condition"

    ReturnToPlay: "Return To Play"
    ReturnToPlay --> PriorityCycle

    %% === TERMINAL STATES (SEPARATED) ===
    Win: "WIN"
    note right of Win
      - "You win the game" effects
      - Last surviving player after opponents lose
    end note
    Win --> [*]

    Lose: "LOSE"
    note right of Lose
      - Life 0 or less
      - Attempts to draw from empty library
      - 10+ poison counters (2HG 15)
      - 21+ combat damage from one commander
      - "Target player loses the game"
      - Concession at any time
    end note
    Lose --> [*]

    GameDraw: "GAME DRAW"
    note right of GameDraw
      - All remaining players lose simultaneously
      - Mandatory loop with no exit
      - Effect says the game is a draw
    end note
    GameDraw --> [*]
