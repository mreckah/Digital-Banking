package com.bank.DigitalBanking.entities;
import com.bank.DigitalBanking.enums.OperationType;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor

public class AccOperation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    private Date operationDate;
    private double amount;
    private OperationType type;
    @ManyToOne
    private BankAcc bankAcc;

}
