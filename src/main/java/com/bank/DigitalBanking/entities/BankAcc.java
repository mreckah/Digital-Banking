package com.bank.DigitalBanking.entities;

import com.bank.DigitalBanking.enums.AccountStatus;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.Date;
import java.util.List;
@Data
@NoArgsConstructor
@AllArgsConstructor
public class BankAcc {
    private String id;
    private double balance;
    private Date createAt;
    private AccountStatus status;
    private Customer customer;
    private List<AccOperation> accOperations;


}
