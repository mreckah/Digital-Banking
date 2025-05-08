package com.bank.DigitalBanking.entities;

import com.bank.DigitalBanking.enums.AccountStatus;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.util.Date;
import java.util.List;
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class BankAcc {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private String id;
    private double balance;
    private Date createAt;
    private AccountStatus status;
    @ManyToOne
    private Customer customer;
    @OneToMany(mappedBy = "bankAcc")
    private List<AccOperation> accOperations;


}
